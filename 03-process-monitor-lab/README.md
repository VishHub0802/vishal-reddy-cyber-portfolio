# Simple Process Monitoring Lab

No Docker, no admin/root permissions needed. Just Python and one library
(`psutil`).

## What this does

A single script (`process_monitor.py`) checks every running process on
the machine every few seconds and flags anything that looks abnormal:

- A process using more CPU than expected
- A process using more memory than expected
- A "zombie" process (one that's finished running but hasn't been
  fully cleaned up by its parent)

Every flagged event gets printed to the terminal and written to a log
file with a timestamp, so there's a record of what happened and when.

This is a simplified, host-based version of the kind of process
monitoring real security tooling does during triage -- watching for
processes that are behaving unusually. It's conceptually related to
things like MITRE ATT&CK's Process Discovery technique, just from the
defender's side: knowing what's normal on a host so you can notice
what isn't.

## Quick concepts (30 seconds)

- **Process** -- a running instance of a program. Every open app, every
  background service, is one or more processes.
- **CPU% / memory%** -- how much of the machine's resources a process
  is currently using. A sudden, sustained spike in either can be a
  sign of a problem (or just a busy app).
- **Zombie process** -- a process that has finished executing, but
  whose exit info hasn't been read by its parent process yet. A few
  are normal; a growing pile of them usually points to a bug
  somewhere.
- **psutil** -- the Python library this script uses to read live
  process info from the operating system.

## Setup

```bash
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash
pip install -r requirements.txt
```

## Run it

```bash
python process_monitor.py
```

The script checks all running processes every 5 seconds and prints
anything flagged, e.g.:

```
[HIGH CPU] chrome.exe (pid 14280) using 112.8% CPU
```

(CPU can go above 100% on multi-core machines -- that just means a
process is using more than one full core's worth of processing power.)

Every flagged event is also written to `alerts.log` with a timestamp,
so there's a persistent record even after the terminal closes. Stop
the script anytime with `Ctrl+C`.

## Sample output

`sample_alerts.log` in this repo is real output from a test run, where
I intentionally loaded a 4K video to spike CPU usage and confirm the
script actually catches it:

```
[2026-09-04 15:49:13] [HIGH CPU] chrome.exe (pid 14280) using 112.8% CPU
[2026-09-04 15:49:23] [HIGH CPU] chrome.exe (pid 14280) using 108.5% CPU
[2026-09-04 15:49:33] [HIGH CPU] chrome.exe (pid 14280) using 135.2% CPU
```

## Things I ran into while building this

- **CPU% reads as 0.0 on the very first check.** `psutil` needs two
  readings spaced apart to calculate a percentage, so the first call
  for any process always returns 0.0. The script "primes" the
  readings once before the real loop starts to avoid this.
- **The script initially flagged itself as high CPU.** Since the
  script is itself a Python process, briefly scanning every process
  on the system used enough CPU to trigger its own alert. Fixed by
  excluding the script's own PID from the checks.
- **Windows' `System Idle Process` reported CPU usage over 1000%.**
  This is a special process representing idle time across all CPU
  cores combined, not a real workload -- excluded by name since it's
  not security-relevant.

## Try it yourself

1. Lower `CPU_THRESHOLD` in the script (e.g. to 10) and re-run --
   notice how much noisier the alerts get. Real monitoring tools have
   to tune this same tradeoff between catching real issues and
   generating false positives.
2. Open Task Manager alongside the script and watch which processes
   get flagged as you open/close applications.
3. Add a new check -- for example, flag any process whose name
   contains a suspicious keyword, a very simplified version of basic
   malware-name heuristics.

## What's next

A natural next step would be comparing each process against its own
historical baseline instead of a single fixed threshold -- so the
script could flag a process that's unusual *for itself*, not just
unusual in general.