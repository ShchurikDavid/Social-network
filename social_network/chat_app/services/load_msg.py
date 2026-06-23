from django.utils.timezone import localtime

def get_msg_list(messages):
    result = []
    last_date = None

    for msg in messages:
        msg_date = localtime(msg.created_at).strftime('%d.%m.%Y')
        if last_date != msg_date:
            result.append({
                'type': 'date-block',
                'date': msg.format_ua_date()
            })
            last_date = msg_date
        result.append(msg)

    return result