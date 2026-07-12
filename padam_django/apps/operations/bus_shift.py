"""
Collection of domain-related functions to work with BusShift
"""


def departure(shift):
    return min(shift.entries.all(), key=__sort_key)


def arrival(shift):
    return max(shift.entries.all(), key=__sort_key)


def departure_stop(shift):
    return departure(shift).bus_stop


def arrival_stop(shift):
    return arrival(shift).bus_stop


def departure_time(shift):
    return departure(shift).arrival_time


def arrival_time(shift):
    return arrival(shift).arrival_time


def duration(shift):
    return arrival_time(shift) - departure_time(shift)


def __sort_key(entry):
    return entry.arrival_time
