import requests
import time
from SPrettify import PrettyLine
history = [] #Atleast 99
base = "http://esper.com"
def main():
    print("Time\tDomain\tClient\tBlocked")
    while True:
        with requests.Session() as session:
            queries = session.get(f"{base}/querylog.json").json()
            for query in reversed(queries):
                if len(history) > 99:
                    history.pop(0)
                if query not in history:
                    history.append(query)
                    line = PrettyLine()
                    # table.define_spacing(20)
                    line.append_text(query['time'], max_spacing=15)
                    if (len(query['domain']) > 50):
                        line.append_text(query['domain'], max_spacing=len(query['domain'])+5)
                    else:
                        line.append_text(query['domain'], max_spacing=50)
                    line.append_text(query['client'], max_spacing=15)
                    line.append_text('Blocked' if query['blocked'] else 'Pass', max_spacing=10)
                    line()
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("--Process end--")