# sms-based-reminder-system
An SMS reminder system that allows users to text a specific number to set reminders for themselves.

## Getting Started

To get the system up and running, follow the steps below:

1). Run the commands below in your terminal:

```bash
git clone git@github.com:aybruhm/sms-based-reminder-system.git
```

2). Change directory to sms-based-reminder-system:

```bash
cd sms-based-reminder-system
```

3). Rename the `.env.template` file to `.env` and update the values.

4). Start the uvicorn server with the below command in your terminal:

```bash
python sms_reminder/main.py
```

**NOTE**: If you get the following error:

```bash
Traceback (most recent call last):
  File "/.../sms-based-reminder-system/sms_reminder/main.py", line 8, in <module>
    from sms_reminder.services.tasks import scheduler
ModuleNotFoundError: No module named 'sms_reminder'
```

Run the below code in your terminal and start your uvicorn server again:

```bash
export PYTHONPATH=$PWD
```
