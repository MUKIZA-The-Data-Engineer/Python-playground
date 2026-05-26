from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class paying_system:
    def __init__(self, course_name,start_course_date, duration_weeks,  first_payment_date_on, ID):
              
            #----inputs ------

        self.ID = "ID"
        self.course_name = "Data Engineering"
        self.start_course_date = datetime (2026, 4, 27)
        self.duration_weeks = 16
        self.first_payment_date_on = datetime(2026, 4, 20)


            #I am going to calculate the end date by adding the number of weeks to the start date
            #we multiply the number of weeks by 7 to get the number of of total days

        course_end_date = start_course_date +timedelta(weeks = duration_weeks)

        payments = []
        urrent_payment_date = first_payment_date_on

        while True:
                period_start = current_payment_date

                period_end = current_payment_date + relativedelta(months = 1) - timedelta(days = 1)

                payments.append({

                    "date": period_start,
                    "until": period_end

                })

                if period_end >= course_end_date:
                    break
                current_payment_date = current_payment_date + relativedelta(months=1)

                #-----OUTPUT -----

                print(f"Course name: {course_name}")
                print(f"Course start date: {start_course_date.strftime('%B %d, %y')}")
                print(f"Course End: {course_end_date.strftime('%B %d, %y')}")
                print("_" * 30)

                for i, p in enumerate(payments):
                    status = "Paid" if i == 0 else "pending"
                    print(f"Payment {i+1}: {p['date'].strftime('%y-%m-%d')} (covers until {p['until'].strftime('%y-%m-%d')}) - {status}")


                print("_" * 30)
                print(f"Total payments to make: {len(payments)} ")