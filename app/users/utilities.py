from app.auth.utilities import verify_psw, hash_psw


def update_information(name, lastName, profile):
    setattr(profile, 'name', name)
    setattr(profile, 'surname', lastName)


def update_password(newPassword, profile):
    setattr(profile, 'password', hash_psw(newPassword))


def sort_by_date(informations):
    ordered_reservations = []
    first_run = True
    informations_copy = informations.copy()
    while len(informations_copy) is not 0:
        for reservation, list in informations_copy.items():
            if first_run:
                first_reservation = reservation
                first_run = False
            if list[0].date < informations_copy[first_reservation][0].date or \
                    (list[0].date == informations_copy[first_reservation][0].date and list[0].morning):
                first_reservation = reservation
        ordered_reservations.append(first_reservation)
        del informations_copy[first_reservation]
        first_run = True
    return ordered_reservations
