#!/usr/bin/env python3
"""
run_ZpTrw_workflow.py
=====================
Automated Z pT reweighting extraction workflow.

The script orchestrates the following steps:

  Pre-Phase 1 — prepare configuration files
  ------------------------------------------
  0a. Patch configuration.py: set tag = "{year}_{sample_type}_{original_tag}"
  0b. Comment out the addSampleWeight line for DY pT reweighting in samples.py
      (weights cannot be applied before they are derived)

  Round 1 — ZpTreweighting analysis
  ----------------------------------
  1a. mkShapesRDF -c 1            compile configuration
  1b. mkShapesRDF -o 0 -f . -b 1  submit HTCondor jobs
  1c. (wait)                       poll condor until all jobs finish
  1d. mkShapesRDF -o 2 -f .        merge individual ROOT files (hadd)
  2.  extract_Zptrw.py             extract the Z pT reweighting function
                                   and overwrite dyZpTrw.json
  2b. Move extract_Zptrw.py plots to plots_{year}_{sample_type}_obtainWeights/
  2c. mkPlot --onlyPlot cratio     create comparison plots on the merged file

  Round 2 — main analysis (optional, --second-analysis DIR)
  ----------------------------------------------------------
  3a. Update DYrew key in aliases.py with the correct year/sample-type
  3b. Uncomment addSampleWeight for DY pT reweighting in samples.py
  3c. mkShapesRDF -c 1            compile second analysis
  3d. mkShapesRDF -o 0 -f . -b 1  submit second-round condor jobs
  3e. (wait)                       poll condor until all jobs finish
  3f. mkShapesRDF -o 2 -f .        merge second-round ROOT files
  3g. mkPlot --onlyPlot cratio     create comparison plots for second round

Prerequisites
-------------
  * Source mkShapesRDF setup first

Typical usage
-------------
  # Run from inside ZpTreweighting/ or give the folder explicitly:
  python automate.py --year 2022 --sample-type LO

  # Also kick off the second-round analysis immediately after:
  python automate.py --year 2022 --sample-type LO --second-analysis ./
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import time


def banner(msg):
    width = max(60, len(msg) + 4)
    print("\n" + "=" * width)
    print(f"  {msg}")
    print("=" * width)


def info(msg):
    print(f"  {msg}")

# Run commands
def run_cmd(cmd, dry_run=False, cwd=None):
    """Print and (optionally) execute *cmd*.

    *cmd* may be a list of strings or a single shell string.
    Returns the process exit code (always 0 in dry-run mode).
    """
    display = " ".join(cmd) if isinstance(cmd, list) else cmd
    info(f"$ {display}")
    if dry_run:
        return 0
    result = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str))
    return result.returncode


def run_cmd_output(cmd, cwd=None):
    """Run *cmd* and return *(returncode, stdout, stderr)* as strings."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        shell=isinstance(cmd, str),
    )
    return result.returncode, result.stdout, result.stderr


# HTCondor job tracking
# Return the set of condor cluster IDs found in the job log files. Log files are expected at ``{batch_dir}/{tag}/**/log.txt``
def _get_cluster_ids_from_logs(batch_dir, tag):
    log_pattern = os.path.join(batch_dir, tag, "**", "log.txt")
    log_files = glob.glob(log_pattern, recursive=True)
    cluster_ids = set()
    for log_file in log_files:
        try:
            with open(log_file) as fh:
                for line in fh:
                    m = re.match(r"000 \((\d+)\.\d+\.\d+\)", line)
                    if m:
                        cluster_ids.add(m.group(1))
        except OSError:
            pass
    return cluster_ids

# Return the number of jobs still in the condor queue for *cluster_id*.
def _count_condor_jobs_in_cluster(cluster_id):
    rc, stdout, _ = run_cmd_output(["condor_q", str(cluster_id)])
    if rc != 0:
        # cluster is gone (all jobs completed or removed)
        return 0
    m = re.search(r"(\d+) jobs?", stdout)
    return int(m.group(1)) if m else 0

# Hold until all HTCondor jobs for *tag* are no longer queued.
def wait_for_condor_jobs(batch_dir, tag, poll_interval=120, dry_run=False):
    CONDOR_REGISTRATION_DELAY = 10

    if dry_run:
        info("[dry-run] Skipping condor wait.")
        return

    # Give HTCondor a few seconds to register newly submitted jobs.
    time.sleep(CONDOR_REGISTRATION_DELAY)

    cluster_ids = _get_cluster_ids_from_logs(batch_dir, tag)
    if not cluster_ids:
        info("WARNING: No condor cluster IDs found in log files. "
             "Waiting 60 s and retrying once...")
        time.sleep(60)
        cluster_ids = _get_cluster_ids_from_logs(batch_dir, tag)

    if not cluster_ids:
        info("WARNING: Still no cluster IDs found. "
             "Assuming jobs have already completed or were submitted "
             "outside HTCondor.")
        return

    info(f"Tracking condor cluster(s): {', '.join(sorted(cluster_ids))}")

    while True:
        remaining = {
            cid for cid in cluster_ids
            if _count_condor_jobs_in_cluster(cid) > 0
        }
        if not remaining:
            info("All condor jobs have completed.")
            return

        total = sum(_count_condor_jobs_in_cluster(c) for c in remaining)
        info(
            f"[{time.strftime('%H:%M:%S')}] "
            f"{total} job(s) still queued in "
            f"cluster(s) {', '.join(sorted(remaining))}. "
            f"Polling again in {poll_interval} s..."
        )
        time.sleep(poll_interval)


# Configuration reader
# Execute *cfg_file* and return a dict with analysis settings.
def read_configuration(cfg_file):
    ns = {
        "__file__": os.path.abspath(cfg_file),
        "os": os,
        "sys": sys,
    }
    try:
        with open(cfg_file) as fh:
            exec(compile(fh.read(), cfg_file, "exec"), ns)
    except Exception as exc:
        # configuration.py may call os.getlogin() which can fail in some
        # environments; fall through with whatever was captured so far.
        info(f"WARNING: Error while parsing {cfg_file}: {exc}")

    tag = ns.get("tag", "ZpTreweighting")
    output_folder = ns.get(
        "outputFolder",
        os.path.join(
            "/eos/user",
            os.environ.get("USER", "unknown")[0],
            os.environ.get("USER", "unknown"),
            "mkShapesRDF_rootfiles",
            tag,
            "rootFile",
        ),
    )
    return {
        "tag":          tag,
        "outputFolder": output_folder.rstrip("/"),
        "outputFile":   ns.get("outputFile", f"mkShapes__{tag}.root"),
        "batchFolder":  ns.get("batchFolder", "condor"),
    }


# Workflow phases
# Phase 1a+1b — compile and submit condor jobs.
def phase1_submit(zptrw_dir, dry_run=False):
    banner("Phase 1a: Compile ZpTreweighting configuration")
    rc = run_cmd(["mkShapesRDF", "-c", "1"], dry_run=dry_run, cwd=zptrw_dir)
    if rc != 0:
        sys.exit(f"ERROR: mkShapesRDF -c 1 failed (exit code {rc})")

    banner("Phase 1b: Submit ZpTreweighting condor jobs")
    rc = run_cmd(
        ["mkShapesRDF", "-o", "0", "-f", ".", "-b", "1"],
        dry_run=dry_run,
        cwd=zptrw_dir,
    )
    if rc != 0:
        sys.exit(f"ERROR: mkShapesRDF -o 0 failed (exit code {rc})")


# Phase 1c — wait for all condor jobs to finish.
def phase1_wait(zptrw_dir, cfg, poll_interval=120, dry_run=False):
    banner("Phase 1c: Waiting for HTCondor jobs to complete")
    batch_dir = os.path.join(zptrw_dir, cfg["batchFolder"])
    wait_for_condor_jobs(
        batch_dir=batch_dir,
        tag=cfg["tag"],
        poll_interval=poll_interval,
        dry_run=dry_run,
    )


# Phase 1d — merge individual job ROOT files (hadd).
def phase1_merge(zptrw_dir, dry_run=False):
    banner("Phase 1d: Merge ROOT files")
    rc = run_cmd(
        ["mkShapesRDF", "-o", "2", "-f", "."],
        dry_run=dry_run,
        cwd=zptrw_dir,
    )
    if rc != 0:
        sys.exit(f"ERROR: Phase 1d - mkShapesRDF -o 2 (merge) failed (exit code {rc})")


# Configuration / samples file patching helpers

# Append '{_suffix}' and prepend '{year}_{sample_type}_' to the tag variable in configuration.py.
def patch_configuration_tag(cfg_file, year, sample_type, suffix, dry_run=False):
    banner("Patching configuration.py: prepending year/sample-type to tag")

    if not os.path.exists(cfg_file):
        info(f"WARNING: {cfg_file} not found; skipping tag patch.")
        return

    with open(cfg_file) as fh:
        content = fh.read()

    prefix = f"{year}_{sample_type}_"
    # Match: tag = "..." or tag = '...' (not already prefixed).
    # Build pattern with f-string so the negative lookahead uses the actual prefix.
    pattern = re.compile(
        r"""^(\s*tag\s*=\s*)["'][^"']*["']""",
        re.MULTILINE,
    )

    def _replace(m):
        new_tag = f'{year}_{sample_type}_ZpTreweighting_{suffix}'
        info(f"  tag: → '{new_tag}'")
        return f'{m.group(1)}"{new_tag}"'

    new_content, count = pattern.subn(_replace, content, count=1)
    if count == 0:
        info("WARNING: Could not find 'tag = ...' line in configuration.py; "
             "skipping tag patch. Verify that configuration.py contains a "
             "tag = \"<name>\" assignment at module level.")
        return

    if not dry_run:
        with open(cfg_file, "w") as fh:
            fh.write(new_content)
        info(f"  Updated: {cfg_file}")
    else:
        info("[dry-run] Would update configuration.py tag.")


# Comment out the addSampleWeight line for DY pT reweighting in samples.py.
def comment_addsampleweight_dy(samples_file, dry_run=False):
    banner("Commenting out addSampleWeight for DY pT reweighting in samples.py")

    if not os.path.exists(samples_file):
        info(f"WARNING: {samples_file} not found; skipping.")
        return

    with open(samples_file) as fh:
        content = fh.read()

    # Match an un-commented addSampleWeight call referencing a DY_*_ZpTrw weight.
    # Pattern breakdown:
    #   ^(?![ \t]*#)           — line must not start with optional whitespace + '#'
    #   ([ \t]*addSampleWeight — capture indentation + function name
    #    \s*\([^)]*            — opening paren and any args
    #    ['"]DY_..._ZpTrw['"] — the DY ZpTrw weight argument
    #    [^)]*\))              — remaining args + closing paren
    pattern = re.compile(
        r"^(?![ \t]*#)([ \t]*addSampleWeight\s*\([^)]*['\"]DY_[A-Za-z0-9]+_ZpTrw['\"][^)]*\))",
        re.MULTILINE,
    )

    if not pattern.search(content):
        info("WARNING: No uncommented addSampleWeight DY ZpTrw line found; skipping.")
        return

    new_content = pattern.sub(r"# \1", content)
    info("  Commented out addSampleWeight DY ZpTrw line.")

    if not dry_run:
        with open(samples_file, "w") as fh:
            fh.write(new_content)
        info(f"  Updated: {samples_file}")
    else:
        info("[dry-run] Would comment out addSampleWeight DY ZpTrw line.")

# Uncomment the addSampleWeight line for DY pT reweighting in samples.py.
def uncomment_addsampleweight_dy(samples_file, dry_run=False):
    banner("Uncommenting addSampleWeight for DY pT reweighting in samples.py")

    if not os.path.exists(samples_file):
        info(f"WARNING: {samples_file} not found; skipping.")
        return

    with open(samples_file) as fh:
        content = fh.read()

    # Match a commented addSampleWeight call referencing a DY_*_ZpTrw weight.
    pattern = re.compile(
        r"^([ \t]*)#[ \t]*(addSampleWeight\s*\([^)]*['\"]DY_[A-Za-z0-9]+_ZpTrw['\"][^)]*\))",
        re.MULTILINE,
    )

    if not pattern.search(content):
        info("WARNING: No commented addSampleWeight DY ZpTrw line found; skipping.")
        return

    new_content = pattern.sub(r"\1\2", content)
    info("  Uncommented addSampleWeight DY ZpTrw line.")

    if not dry_run:
        with open(samples_file, "w") as fh:
            fh.write(new_content)
        info(f"  Updated: {samples_file}")
    else:
        info("[dry-run] Would uncomment addSampleWeight DY ZpTrw line.")

# Replace DYrew['old_year']['old_type'] with DYrew['{year}']['{sample_type}'] in aliases.py.
def update_aliases_dyrew_key(aliases_file, year, sample_type, dry_run=False):
    banner(f"Updating DYrew key in {os.path.basename(aliases_file)}")

    if not os.path.exists(aliases_file):
        info(f"WARNING: {aliases_file} not found; skipping DYrew key update.")
        return

    with open(aliases_file) as fh:
        content = fh.read()

    # Match DYrew['oldyear']['oldtype_jetbin'] or DYrew["oldyear"]["oldtype_jetbin"]
    pattern = re.compile(
        r"""DYrew\[\s*(['"])[^'"]+\1\s*\]\[\s*(['"])[^'"]+_(0j|1j|2j)\2\s*\]"""
    )

    def replacer(match):
        quote1, quote2, jetbin = match.group(1), match.group(2), match.group(3)
        return f"DYrew[{quote1}{year}{quote1}][{quote2}{sample_type}_{jetbin}{quote2}]"

    matches = pattern.findall(content)
    if not matches:
        info(f"No DYrew['...']['...'] references found in {aliases_file}; skipping.")
        return

    new_content = pattern.sub(replacer, content)
    info(f"  Updated {len(matches)} DYrew key reference(s) → ['{year}']['{sample_type}_<jetbin>']")

    if not dry_run:
        with open(aliases_file, "w") as fh:
            fh.write(new_content)
        info(f"  Updated: {aliases_file}")
    else:
        info(f"[dry-run] Would update DYrew key in {aliases_file}.")

# Plot helpers
# Move plots produced by extract_Zptrw.py into plots_{year}_{sample_type}_obtainWeights/.
def move_zptrw_plots(zptrw_dir, year, sample_type, folder_suffix="", dry_run=False):
    banner("Moving extract_Zptrw.py plots to archive folder")

    target_dir = os.path.join(zptrw_dir, f"extractPlots_{year}_{sample_type}_{folder_suffix}")
    plot_files = (
        glob.glob(os.path.join(zptrw_dir, "ZpTreweighting_*.pdf"))
        + glob.glob(os.path.join(zptrw_dir, "ZpTreweighting_*.png"))
    )

    if not plot_files:
        info("No ZpTreweighting_*.pdf/png files found to move.")
        return

    info(f"Target folder: {target_dir}")
    for src in plot_files:
        dest = os.path.join(target_dir, os.path.basename(src))
        info(f"  {os.path.basename(src)} → {os.path.relpath(dest, zptrw_dir)}")
        if not dry_run:
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(src, dest)

    if dry_run:
        info("[dry-run] Would create target folder and move plot files.")

# Run ``mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png``.
def run_mkplot(analysis_dir, dry_run=False):
    banner(f"Running mkPlot in {analysis_dir}")
    rc = run_cmd(
        ["mkPlot", "--onlyPlot", "cratio", "--showIntegralLegend", "1",
         "--fileFormats", "png"],
        dry_run=dry_run,
        cwd=analysis_dir,
    )
    if rc != 0:
        info(f"WARNING: mkPlot exited with code {rc}. Continuing workflow.")

# Phase 2 — run extract_Zptrw.py to derive weights and update dyZpTrw.json, or make the ratio plots after applying the weights.
def phase2_extract(zptrw_dir, cfg, year="2022", sample_type="LO", run_fit = "", dry_run=False):
    banner("Phase 2: Extract Z pT reweighting function → update dyZpTrw.json")

    merged_file = os.path.join(cfg["outputFolder"], cfg["outputFile"])
    dyzptrw_json = os.path.join(zptrw_dir, "dyZpTrw.json")
    extract_script = os.path.join(zptrw_dir, "extract_Zptrw.py")

    if not dry_run and not os.path.exists(merged_file):
        sys.exit(
            f"ERROR: Merged ROOT file not found:\n"
            f"  {merged_file}\n"
            f"Run 'mkShapesRDF -o 2 -f .' in {zptrw_dir} first."
        )
    for njet in [0, 1, 2]:
        # derive weights in Z->MuMu channel, 0 jet bin
        if run_fit == "-f":
            # define normalization when fitting is requested, else, just plot
            cmd = [sys.executable, extract_script, "-f", "-n", "2", "-c", "mm", "-nj", str(njet), "--input", merged_file, "--write-json", dyzptrw_json, "--year", year, "--sample-type", sample_type]
        else:
            cmd = [sys.executable, extract_script, "-c", "mm", "-nj", str(njet), "--input", merged_file, "--write-json", dyzptrw_json, "--year", year, "--sample-type", sample_type]
        rc = run_cmd(cmd, dry_run=dry_run, cwd=zptrw_dir)
        # Make plots in Z->ee channel, 0 jet bin
        cmd = [sys.executable, extract_script, "-c", "ee", "-nj", str(njet), "--input", merged_file]
        rc = run_cmd(cmd, dry_run=dry_run, cwd=zptrw_dir)
        if rc != 0:
            sys.exit(f"ERROR: extract_Zptrw.py failed (exit code {rc})")
        info(f"dyZpTrw.json updated for nJet={njet} → {dyzptrw_json}")

# Phase 3 — prepare, compile, submit, wait, merge, and plot second-round analysis.
def phase3_second_round(second_dir, year, sample_type, poll_interval=120,
                        skip_second_wait=False, skip_second_merge=False,
                        dry_run=False):
    banner(f"Phase 3: Second-round mkShapesRDF in\n  {second_dir}")

    # Update aliases.py and samples.py before compiling
    aliases_file = os.path.join(second_dir, "aliases.py")
    update_aliases_dyrew_key(aliases_file, year, sample_type, dry_run=dry_run)

    samples_file = os.path.join(second_dir, "samples.py")
    uncomment_addsampleweight_dy(samples_file, dry_run=dry_run)

    rc = run_cmd(["mkShapesRDF", "-c", "1"], dry_run=dry_run, cwd=second_dir)
    if rc != 0:
        sys.exit(
            f"ERROR: mkShapesRDF -c 1 failed in {second_dir} (exit code {rc})"
        )

    rc = run_cmd(
        ["mkShapesRDF", "-o", "0", "-f", ".", "-b", "1"],
        dry_run=dry_run,
        cwd=second_dir,
    )
    if rc != 0:
        sys.exit(
            f"ERROR: mkShapesRDF -o 0 failed in {second_dir} (exit code {rc})"
        )

    # Wait for second-round condor jobs
    second_cfg_file = os.path.join(second_dir, "configuration.py")
    has_cfg = os.path.exists(second_cfg_file)

    if not skip_second_wait:
        if has_cfg or dry_run:
            banner("Phase 3c: Waiting for second-round HTCondor jobs to complete")
            second_cfg = (
                read_configuration(second_cfg_file)
                if has_cfg
                else {"tag": "unknown", "batchFolder": "condor",
                      "outputFolder": ".", "outputFile": "output.root"}
            )
            batch_dir = os.path.join(second_dir, second_cfg["batchFolder"])
            wait_for_condor_jobs(
                batch_dir=batch_dir,
                tag=second_cfg["tag"],
                poll_interval=poll_interval,
                dry_run=dry_run,
            )
        else:
            info(f"WARNING: No configuration.py found in {second_dir}; "
                 "skipping second-round condor wait.")
    else:
        info("\n[skip-second-wait] Skipping second-round condor wait.")

    # Merge second-round ROOT files
    if not skip_second_merge:
        banner("Phase 3d: Merge second-round ROOT files")
        rc = run_cmd(
            ["mkShapesRDF", "-o", "2", "-f", "."],
            dry_run=dry_run,
            cwd=second_dir,
        )
        if rc != 0:
            sys.exit(
                f"ERROR: mkShapesRDF -o 2 (merge) failed in {second_dir} "
                f"(exit code {rc})"
            )
    else:
        info("\n[skip-second-merge] Skipping second-round ROOT file merge.")

    # Create RDF plots for the second-round merged output
    run_mkplot(second_dir, dry_run=dry_run)


# CLI
def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # ---- paths ----
    parser.add_argument(
        "--zptrw-folder",
        default=".",
        metavar="DIR",
        help="Path to the ZpTreweighting analysis folder "
             "(default: current directory).",
    )
    parser.add_argument(
        "--second-analysis",
        default=None,
        metavar="DIR",
        help="Path to the second-round analysis folder. "
             "When given, Phase 3 updates aliases/samples, compiles, submits, "
             "waits, merges, and runs mkPlot there after dyZpTrw.py has been updated.",
    )

    # ---- physics ----
    parser.add_argument(
        "--year",
        default="2022",
        help="Year key written to DYrew in dyZpTrw.json (default: '2022').",
    )
    parser.add_argument(
        "--sample-type",
        default="LO",
        help="Sample-type key written to DYrew in dyZpTrw.json "
             "(default: 'LO').",
    )

    # ---- condor polling ----
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=120,
        metavar="SECONDS",
        help="Seconds between condor_q polls while waiting for jobs "
             "(default: 120).",
    )

    # ---- skip flags ----
    skip = parser.add_argument_group("skip flags (for re-running partial workflow)")
    skip.add_argument(
        "--skip-submit",
        action="store_true",
        help="Skip Phase 1a+1b (assume jobs are already running or done).",
    )
    skip.add_argument(
        "--skip-wait",
        action="store_true",
        help="Skip Phase 1c (assume all jobs have already finished).",
    )
    skip.add_argument(
        "--skip-merge",
        action="store_true",
        help="Skip Phase 1d (assume the merged ROOT file already exists).",
    )
    skip.add_argument(
        "--skip-extract",
        action="store_true",
        help="Skip Phase 2 (assume dyZpTrw.json is already up to date).",
    )
    skip.add_argument(
        "--skip-second-wait",
        action="store_true",
        help="Skip waiting for second-round HTCondor jobs (Phase 3c).",
    )
    skip.add_argument(
        "--skip-second-merge",
        action="store_true",
        help="Skip merging second-round ROOT files (Phase 3d).",
    )

    # ---- misc ----
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print every command that would be run without executing it.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    zptrw_dir = os.path.abspath(args.zptrw_folder)
    if not os.path.isdir(zptrw_dir):
        sys.exit(f"ERROR: ZpTreweighting folder not found: {zptrw_dir}")

    cfg_file = os.path.join(zptrw_dir, "configuration.py")
    if not os.path.exists(cfg_file):
        sys.exit(f"ERROR: configuration.py not found in {zptrw_dir}")

    banner("Z pT reweighting workflow")
    info(f"ZpTreweighting folder : {zptrw_dir}")
    if args.dry_run:
        info("*** DRY-RUN mode — no commands will be executed ***")

    # ---- Pre-Phase 1: Patch configuration.py tag and comment out DY pT rw weight ----
    patch_configuration_tag(cfg_file, args.year, args.sample_type, suffix="obtainWeights", dry_run=args.dry_run)

    cfg = read_configuration(cfg_file)
    info(f"tag          : {cfg['tag']}")
    info(f"outputFolder : {cfg['outputFolder']}")
    info(f"outputFile   : {cfg['outputFile']}")
    info(f"batchFolder  : {cfg['batchFolder']}")

    samples_file = os.path.join(zptrw_dir, "samples.py")
    comment_addsampleweight_dy(samples_file, dry_run=args.dry_run)

    # ---- Phase 1a+1b: Submit ----
    if not args.skip_submit:
        phase1_submit(zptrw_dir, dry_run=args.dry_run)
    else:
        info("\n[skip-submit] Skipping job submission.")

    # ---- Phase 1c: Wait ----
    if not args.skip_wait and not args.skip_submit:
        phase1_wait(
            zptrw_dir,
            cfg,
            poll_interval=args.poll_interval,
            dry_run=args.dry_run,
        )
    elif args.skip_wait:
        info("\n[skip-wait] Skipping condor wait.")

    # ---- Phase 1d: Merge ----
    if not args.skip_merge:
        phase1_merge(zptrw_dir, dry_run=args.dry_run)
    else:
        info("\n[skip-merge] Skipping ROOT file merge.")

    # ---- Phase 2: Extract + Update ----
    if not args.skip_extract:
        phase2_extract(zptrw_dir, cfg, year=args.year, sample_type=args.sample_type, run_fit="-f", dry_run=args.dry_run)
        # Move plots produced by extract_Zptrw.py to archive folder
        move_zptrw_plots(zptrw_dir, args.year, args.sample_type, folder_suffix = "obtainWeights", dry_run=args.dry_run)
        # Create RDF plots from the merged ROOT file
        run_mkplot(zptrw_dir, dry_run=args.dry_run)
        # Rename condor and config folders:
        cmd = ["mv", os.path.join(zptrw_dir, "condor/"), os.path.join(zptrw_dir, f"condor_{args.year}_{args.sample_type}_obtainWeights")]
        rc = run_cmd(cmd, cwd=zptrw_dir)
        if rc != 0:
            sys.exit(f"ERROR: failed to rename condor directory (exit code {rc})")
        cmd = ["pwd"]
        rc = run_cmd(cmd, cwd=zptrw_dir)
        cmd = ["mv", os.path.join(zptrw_dir, "configs/"), os.path.join(zptrw_dir, f"configs_{args.year}_{args.sample_type}_obtainWeights")]
        rc = run_cmd(cmd, cwd=zptrw_dir)
        if rc != 0:
            sys.exit(f"ERROR: failed to rename configs directory (exit code {rc})")

    else:
        info("\n[skip-extract] Skipping weight extraction, plot archiving, and mkPlot "
             "(assumes dyZpTrw.json and plots are already up to date).")

    # ---- Phase 3 (optional): Second analysis ----
    if args.second_analysis:
        second_dir = os.path.abspath(args.second_analysis)
        if not os.path.isdir(second_dir):
            sys.exit(f"ERROR: Second-analysis folder not found: {second_dir}")

        patch_configuration_tag(cfg_file, args.year, args.sample_type, suffix="afterReweighting", dry_run=args.dry_run)
        cfg = read_configuration(cfg_file)
        info(f"tag          : {cfg['tag']}")
        info(f"outputFolder : {cfg['outputFolder']}")
        info(f"outputFile   : {cfg['outputFile']}")
        info(f"batchFolder  : {cfg['batchFolder']}")

        phase3_second_round(
            second_dir,
            year=args.year,
            sample_type=args.sample_type,
            poll_interval=args.poll_interval,
            skip_second_wait=args.skip_second_wait,
            skip_second_merge=args.skip_second_merge,
            dry_run=args.dry_run,
        )
        phase2_extract(zptrw_dir, cfg, year=args.year, sample_type=args.sample_type, run_fit="", dry_run=args.dry_run)
        # Move plots produced by extract_Zptrw.py to folder
        move_zptrw_plots(zptrw_dir, args.year, args.sample_type, folder_suffix = "afterReweighting", dry_run=args.dry_run)
        # Create comparison plots from the merged ROOT file
        run_mkplot(zptrw_dir, dry_run=args.dry_run)
        # Rename log, condor, and config folders:
        cmd = ["mv", os.path.join(zptrw_dir, "condor/"), os.path.join(zptrw_dir, f"condor_{args.year}_{args.sample_type}_afterReweighting")]
        rc = run_cmd(cmd, cwd=zptrw_dir)
        if rc != 0:
            sys.exit(f"ERROR: failed to rename condor directory (exit code {rc})")
        cmd = ["mv", os.path.join(zptrw_dir, "configs/"), os.path.join(zptrw_dir, f"configs_{args.year}_{args.sample_type}_afterReweighting")]
        rc = run_cmd(cmd, cwd=zptrw_dir)
        if rc != 0:
            sys.exit(f"ERROR: failed to rename configs directory (exit code {rc})")

    banner("Workflow complete!")
    if args.second_analysis:
        info("Second-round analysis finished. Plots are in the analysis folder.")
    else:
        info("dyZpTrw.json has been updated.")
        info("To run the second-round analysis:")
        info("  cd <your-analysis-folder>")
        info("  mkShapesRDF -c 1")
        info("  mkShapesRDF -o 0 -f . -b 1")


if __name__ == "__main__":
    main()