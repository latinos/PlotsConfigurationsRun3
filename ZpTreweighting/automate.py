#!/usr/bin/env python3
"""
run_ZpTrw_workflow.py
=====================
Automated Z pT reweighting extraction workflow.

The script orchestrates the following steps:

  Round 1 — ZpTreweighting analysis
  ----------------------------------
  1a. mkShapesRDF -c 1            compile configuration
  1b. mkShapesRDF -o 0 -f . -b 1  submit HTCondor jobs
  1c. (wait)                       poll condor until all jobs finish
  1d. mkShapesRDF -o 2 -f .        merge individual ROOT files (hadd)
  2.  extract_Zptrw.py             extract the Z pT reweighting function
                                   and overwrite dyZpTrw.json

  Round 2 — main analysis (optional)
  -----------------------------------
  3a. mkShapesRDF -c 1            compile second analysis
  3b. mkShapesRDF -o 0 -f . -b 1  submit second-round condor jobs

Prerequisites
-------------
  * mkShapesRDF must be on PATH (source the mkShapesRDF start.sh first).
  * The merged ROOT output lives on EOS; EOS must be mounted (lxplus default).
  * Python packages required by extract_Zptrw.py must be available (ROOT,
    mplhep, matplotlib, numpy).

Typical usage
-------------
  # Run from inside ZpTreweighting/ or give the folder explicitly:
  python run_ZpTrw_workflow.py

  # Also kick off the second-round analysis immediately after:
  python run_ZpTrw_workflow.py --second-analysis ../HWW/ggH_SF/2022

  # Skip submission if jobs were already submitted:
  python run_ZpTrw_workflow.py --skip-submit

  # Dry run to see what commands would be executed:
  python run_ZpTrw_workflow.py --dry-run
"""

import argparse
import glob
import os
import re
import subprocess
import sys
import time


# ---------------------------------------------------------------------------
# Pretty printing helpers
# ---------------------------------------------------------------------------

def banner(msg):
    width = max(60, len(msg) + 4)
    print("\n" + "=" * width)
    print(f"  {msg}")
    print("=" * width)


def info(msg):
    print(f"  {msg}")


# ---------------------------------------------------------------------------
# Command execution
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# HTCondor job tracking
# ---------------------------------------------------------------------------

def _get_cluster_ids_from_logs(batch_dir, tag):
    """Return the set of condor cluster IDs found in the job log files.

    Log files are expected at ``{batch_dir}/{tag}/**/log.txt`` (the standard
    layout produced by mkShapesRDF).  The cluster ID is extracted from lines
    matching the condor event-log format::

        000 (CLUSTERID.PROCID.SUBPROCID) DATE TIME Job submitted from host...
    """
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


def _count_condor_jobs_in_cluster(cluster_id):
    """Return the number of jobs still in the condor queue for *cluster_id*.

    Runs ``condor_q <cluster_id>`` and parses the summary line, e.g.::

        3 jobs; 0 completed; 0 removed; 3 idle; 0 running; 0 held; 0 suspended
    """
    rc, stdout, _ = run_cmd_output(["condor_q", str(cluster_id)])
    if rc != 0:
        # cluster is gone (all jobs completed or removed)
        return 0
    m = re.search(r"(\d+) jobs?", stdout)
    return int(m.group(1)) if m else 0


def wait_for_condor_jobs(batch_dir, tag, poll_interval=120, dry_run=False):
    """Block until all HTCondor jobs for *tag* are no longer queued.

    Parameters
    ----------
    batch_dir:
        Directory that contains the ``{tag}/`` sub-tree of condor job folders.
    tag:
        Analysis tag (matches the sub-directory name inside ``batch_dir``).
    poll_interval:
        Seconds to wait between condor_q polls.
    dry_run:
        If True, return immediately without checking anything.
    """
    # Seconds to wait after submission before the first condor_q poll, so
    # HTCondor has time to register the newly submitted jobs.
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


# ---------------------------------------------------------------------------
# Configuration reader
# ---------------------------------------------------------------------------

def read_configuration(cfg_file):
    """Execute *cfg_file* and return a dict with analysis settings.

    Reads ``tag``, ``outputFolder``, ``outputFile``, and ``batchFolder``
    from ``configuration.py``.
    """
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


# ---------------------------------------------------------------------------
# Workflow phases
# ---------------------------------------------------------------------------

def phase1_submit(zptrw_dir, dry_run=False):
    """Phase 1a+1b — compile and submit condor jobs."""
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


def phase1_wait(zptrw_dir, cfg, poll_interval=120, dry_run=False):
    """Phase 1c — wait for all condor jobs to finish."""
    banner("Phase 1c: Waiting for HTCondor jobs to complete")
    batch_dir = os.path.join(zptrw_dir, cfg["batchFolder"])
    wait_for_condor_jobs(
        batch_dir=batch_dir,
        tag=cfg["tag"],
        poll_interval=poll_interval,
        dry_run=dry_run,
    )


def phase1_merge(zptrw_dir, dry_run=False):
    """Phase 1d — merge individual job ROOT files (hadd)."""
    banner("Phase 1d: Merge ROOT files")
    rc = run_cmd(
        ["mkShapesRDF", "-o", "2", "-f", "."],
        dry_run=dry_run,
        cwd=zptrw_dir,
    )
    if rc != 0:
        sys.exit(f"ERROR: Phase 1d - mkShapesRDF -o 2 (merge) failed (exit code {rc})")


def phase2_extract(zptrw_dir, cfg, year="2022", sample_type="LO", dry_run=False):
    """Phase 2 — run extract_Zptrw.py to derive weights and update dyZpTrw.json."""
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

    cmd = [
        sys.executable, extract_script,
        "-f",
        "--input",      merged_file,
        "--write-json", dyzptrw_json,
        "--year",       year,
        "--sample-type", sample_type,
    ]
    rc = run_cmd(cmd, dry_run=dry_run, cwd=zptrw_dir)
    if rc != 0:
        sys.exit(f"ERROR: extract_Zptrw.py failed (exit code {rc})")

    info(f"dyZpTrw.json updated → {dyzptrw_json}")


def phase3_second_round(second_dir, dry_run=False):
    """Phase 3 — compile and submit the second-round analysis."""
    banner(f"Phase 3: Second-round mkShapesRDF in\n  {second_dir}")

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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

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
        default=".",
        metavar="DIR",
        help="Path to the second-round analysis folder. "
             "When given, Phase 3 compiles and submits jobs there after "
             "dyZpTrw.py has been updated.",
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

    # ---- misc ----
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print every command that would be run without executing it.",
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

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

    cfg = read_configuration(cfg_file)
    info(f"tag          : {cfg['tag']}")
    info(f"outputFolder : {cfg['outputFolder']}")
    info(f"outputFile   : {cfg['outputFile']}")
    info(f"batchFolder  : {cfg['batchFolder']}")

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
        phase2_extract(
            zptrw_dir,
            cfg,
            year=args.year,
            sample_type=args.sample_type,
            dry_run=args.dry_run,
        )
    else:
        info("\n[skip-extract] Skipping weight extraction and dyZpTrw.json update.")

    # ---- Phase 3 (optional): Second analysis ----
    if args.second_analysis:
        second_dir = os.path.abspath(args.second_analysis)
        if not os.path.isdir(second_dir):
            sys.exit(f"ERROR: Second-analysis folder not found: {second_dir}")
        phase3_second_round(second_dir, dry_run=args.dry_run)

    banner("Workflow complete!")
    if args.second_analysis:
        info("Second-round jobs submitted. Next steps:")
        info(f"  Monitor : mkShapesRDF -o 1 -f {args.second_analysis}")
        info(f"  Merge   : mkShapesRDF -o 2 -f {args.second_analysis}")
    else:
        info("dyZpTrw.json has been updated.")
        info("To run the second-round analysis:")
        info("  cd <your-analysis-folder>")
        info("  mkShapesRDF -c 1")
        info("  mkShapesRDF -o 0 -f . -b 1")


if __name__ == "__main__":
    main()