import csv
import StringIO


def generate_audition_session_csv(session):
    csvfile = StringIO.StringIO()
    header = (
        'Slot Time',
        'First Name',
        'Last Name',
        'Email',
        'Phone',
        'Act Description',
        'Prop A/V Needs',
    )
    slots = session.auditionslot_set.order_by('start_time')
    rows = [slot.as_csv_dict() for slot in slots]
    writer = csv.DictWriter(csvfile, header)
    writer.writeheader()
    writer.writerows(rows)
    return csvfile