# Author: Ilya V. Schurov (ilya@schurov.com), with the kind help of ChatGPT (GPT-4)
# License: MIT

import curses
import subprocess
import threading
import time
import os


class SlurmJobController:
    def __init__(self, screen):
        self.screen = screen
        self.jobs = []
        self.header = ""
        self.selected_index = 0
        self.lock = threading.Lock()
        self.prev_job_count = 0

    def fetch_jobs(self):
        """Fetch current SLURM jobs using squeue command."""
        result = subprocess.run(["squeue", "--me"], capture_output=True, text=True)
        return result.stdout.rstrip().split("\n")

    def update_job_list(self):
        i = 0
        while True:
            i += 1
            self.update_job_list_once()
            time.sleep(1)  # Refresh interval

    def update_job_list_once(self):
        """Fetch jobs once and update the list."""
        header, *new_jobs = self.fetch_jobs()
        with self.lock:
            self.jobs = new_jobs
            self.header = header

    def display_minihelp(self):
        height, width = self.screen.getmaxyx()
        self.screen.addstr(
            height - 1,
            4,
            "Q: quit   C: cancel   ↓ | J: down   ↑ | K: up   L: less   T: tail",
        )
        self.screen.clrtoeol()
        self.screen.refresh()

    def display_jobs(self):
        """Optimized display of jobs."""
        with self.lock:
            max_y, max_x = self.screen.getmaxyx()
            current_jobs = len(self.jobs)

            self.screen.addstr(1, 4, self.header)

            # Update only the lines that have changed
            for i in range(max(current_jobs, self.prev_job_count)):
                if i < current_jobs:
                    if i == self.selected_index:
                        self.screen.attron(curses.A_REVERSE)
                        self.screen.addstr(i + 2, 4, self.jobs[i][: max_x - 1])
                        self.screen.attroff(curses.A_REVERSE)
                    else:
                        self.screen.addstr(i + 2, 4, self.jobs[i][: max_x - 1])
                else:
                    self.screen.move(i + 2, 0)
                    self.screen.clrtoeol()  # Clear residual text from previous longer lists

            self.prev_job_count = current_jobs
            self.screen.refresh()

    def show_message(self, message, sleep=1):
        """Display an error message at the bottom of the screen."""
        height, width = self.screen.getmaxyx()
        self.screen.addstr(height - 2, 4, message)
        self.screen.clrtoeol()
        self.screen.refresh()
        time.sleep(sleep)

    def run_system_command(self, command):
        """Run a system command and restore terminal settings afterwards."""
        # Turn off curses operations, save the current terminal state
        curses.endwin()
        os.system(command)
        # Restore the screen and terminal settings
        self.screen.clear()
        self.display_minihelp()
        curses.doupdate()

    def cancel_job(self, selected_job):
        self.show_message(
            f"Cancelling job {selected_job}, Press any key to abort",
            sleep=2,
        )
        if self.screen.getch() != -1:
            self.show_message("Aborted")
            return
        try:
            subprocess.run(["scancel", selected_job], check=True)
            self.show_message(f"Cancelled job {selected_job}")
        except subprocess.CalledProcessError as e:
            self.show_message(f"Failed to cancel job {selected_job}: {e}")

    def key_event_handler(self):
        self.screen.nodelay(True)
        sleep_time = 0.1

        self.display_jobs()
        while True:
            try:
                key = self.screen.getch()
                if key != -1:
                    if key == ord("q") or key == ord("Q"):
                        break
                    if key == curses.KEY_RESIZE:
                        # Redraw the interface for the new window size
                        self.screen.clear()
                        self.display_jobs()
                        self.display_minihelp()
                        continue
                    if (
                        key == curses.KEY_UP or key == ord("k")
                    ) and self.selected_index > 0:
                        self.selected_index -= 1
                    elif (
                        key == curses.KEY_DOWN or key == ord("j")
                    ) and self.selected_index < len(self.jobs) - 1:
                        self.selected_index += 1
                    else:
                        selected_job = self.jobs[self.selected_index].split()[0]
                        output_file = f"slurm-{selected_job}.out"
                        if key == ord("c") or key == ord("C"):
                            self.cancel_job(selected_job)
                        elif key in (
                            ord("l"),
                            ord("t"),
                            ord("L"),
                            ord("T"),
                        ) and not os.path.exists(output_file):
                            self.show_message(
                                f"Output file {output_file} does not exist."
                            )
                        elif key == ord("l") or key == ord("L"):
                            self.run_system_command(f"less {output_file}")
                        elif key == ord("t") or key == ord("T"):
                            self.run_system_command(f"tail -f {output_file}")

                self.display_jobs()
                time.sleep(sleep_time)

            except KeyboardInterrupt:
                break


def main(screen):
    curses.curs_set(0)  # Hide cursor
    controller = SlurmJobController(screen)

    controller.display_minihelp()
    controller.update_job_list_once()

    # Start a separate thread to continuously fetch jobs
    job_thread = threading.Thread(target=controller.update_job_list, daemon=True)
    job_thread.start()

    controller.key_event_handler()


def run():
    curses.wrapper(main)


if __name__ == "__main__":
    run()
