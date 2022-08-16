"""
filename: scheduler.py
"""

import os
import heapq


def difference_scheduling(jobs, jobs_size):
    """Returns a scheduling based on weight - length in decreasing order"""
    schedule = []
    ordered_schedule = []
    for i in range(jobs_size):
        heapq.heappush(
            schedule, ((jobs[i][0]-jobs[i][1]) * -1, [jobs[i][0] * -1, jobs[i][1]]))
    while schedule:
        job = heapq.heappop(schedule)
        ordered_schedule.append([job[0]*-1, (job[1][0] * -1, job[1][1])])
    return ordered_schedule


def ratio_scheduling(jobs, jobs_size):
    """Returns a scheduling based on weight/length in decreasing order"""
    schedule = []
    ordered_schedule = []
    for i in range(jobs_size):
        heapq.heappush(
            schedule, ((jobs[i][0]/jobs[i][1]) * -1, [jobs[i][0] * -1, jobs[i][1]]))
    while schedule:
        job = heapq.heappop(schedule)
        ordered_schedule.append([job[0]*-1, (job[1][0] * -1, job[1][1])])
    return ordered_schedule


def calc_work(schedule, job_size):
    """Given a schedule calculates the total amount of work time by the jobs"""
    completion_time = 0
    work = 0
    for i in range(job_size):
        completion_time += schedule[i][1][1]
        work += completion_time * schedule[i][1][0]
    print(f'Total work: {work}')


def main():
    """main method"""
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("../input/jobs.txt", cur_path)
    f = open(new_path, "r", encoding="utf-8")
    lines = f.readlines()
    jobs = []
    jobs_size = int(lines[0])
    for i in lines[1:]:
        job = i.strip().split()
        jobs.append([int(job[0]), int(job[1])])
    f.close()
    # test = [[3, 1], [2, 2], [1, 3]]
    # test_size = 3
    # test = [[3, 5], [1, 2]]
    # test_size = 2

    diff_schedule = difference_scheduling(jobs, jobs_size)
    calc_work(diff_schedule, jobs_size)

    ratio_schedule = ratio_scheduling(jobs, jobs_size)
    calc_work(ratio_schedule, jobs_size)


if __name__ == "__main__":
    main()
