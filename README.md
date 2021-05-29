# Check-Vaccine-Slots

This is for windows operatiing system only, for now.

Pre-requisites :- Install winrt and hyper.

pip install hyper
pip install winrt

To execute the python file, run it like this.

python cowin_vaccine_slots.py <date in dd-mm-yyyy format> <district_id> <frequency to check per minute> <minimum vaccine slots available to notify for 18-44> <minimum vaccine slots available to notify for 45+> <preferred vaccine slot (1st or 2nd)> <preferred vaccine>
  
Minimum vaccine slots :- Minimum number of slots available to be notified. -1 if a category(18-44 or 45+) needs to be ignored.
  
Preferred vaccine slot :- 
* 0 - No preferred slot.
* 1 - Check for 1st dose.
* 2 - Check for 2nd dose.

Preferred Vaccine :-
* Covishield, Covaxin or Both.
