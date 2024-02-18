IP = r"((?:\d{1,3}\.?){4})"
DATE = r"\[([^\]]+)\]"
STRING = r"\"([^\"]+)\""
STATUS = r"(\d{3})"
SIZE = r"(\d+)"

NGINX_LOG_LINE = rf"{IP} - - {DATE} {STRING} {STATUS} {SIZE} {STRING} {STRING} \"-\""
