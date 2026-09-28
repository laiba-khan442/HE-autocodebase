# HalalEats Appium Python Tests

This project contains automated Android tests for the complete HalalEats application suite. It uses Python and pytest to define and run tests, while Appium and the UiAutomator2 driver communicate with a physical Android device.

Each application has its own package, activity, and test folder. Device-specific values such as the `udid` must be set for the phone being used.

## How the Setup Works

- Python contains the test code.
- pytest discovers, runs, and reports the tests.
- Appium-Python-Client sends commands from Python to the Appium server.
- The Appium server receives the commands and passes them to UiAutomator2.
- UiAutomator2 controls the Android application on the connected phone.
- ADB confirms that the computer can communicate with the phone.
- Appium Inspector is optional and helps identify screen elements.

## General Appium Configuration

| Setting | Current value |
| --- | --- |
| Platform | Android |
| Automation driver | UiAutomator2 |
| Device name | `Android Device` |
| Device UDID | `<DEVICE_UDID>` |
| Application package | `<APP_PACKAGE>` |
| Application activity | `<APP_ACTIVITY>` |
| Appium server URL | `http://127.0.0.1:4723` |

If another device is used, find its UDID with:

```powershell
adb devices -l
```

## One-Time Machine Setup

The following steps are required only when preparing a new Windows computer.

### 1. Install Git

Install Git for Windows and verify it in PowerShell:

```powershell
git --version
```

### 2. Install Python

Install Python and ensure the Python launcher works:

```powershell
py --version
```

The current project has been tested with Python 3.13.15.

If typing `python` opens the Microsoft Store or reports that Python cannot be found, use the `py` launcher or the Python executable inside `.venv` as shown later in this guide.

### 3. Install Node.js and npm

Appium runs on Node.js even though the tests are written in Python. Install a current Appium-compatible Node.js release and verify both tools:

```powershell
node --version
npm --version
```

The project does not require a `node_modules` folder inside the test directory when Appium is installed globally.

### 4. Install Java

Android automation requires Java. Android Studio includes a suitable Java Runtime in its `jbr` directory.

The current `JAVA_HOME` value is:

```text
C:\Program Files\Android\Android Studio\jbr
```

Verify Java:

```powershell
$env:JAVA_HOME
java -version
Test-Path "$env:JAVA_HOME\bin\java.exe"
```

The final command should return `True`.

### 5. Install Android Studio and Android SDK Components

Install Android Studio. In Android Studio's SDK Manager, ensure these components are installed:

- Android SDK Platform-Tools
- Android SDK Command-line Tools (latest)
- At least one Android SDK Platform compatible with the test device/application
- Android SDK Build-Tools

An Android Emulator is not required when all testing is performed on a physical device. Appium Doctor may still display an emulator warning; that warning can be ignored for this setup.

A typical Android SDK location is:

```text
C:\Users\<WINDOWS_USERNAME>\AppData\Local\Android\Sdk
```

Set `ANDROID_HOME` to that SDK directory and add these directories to the Windows `Path`:

```text
C:\Users\<WINDOWS_USERNAME>\AppData\Local\Android\Sdk\platform-tools
C:\Users\<WINDOWS_USERNAME>\AppData\Local\Android\Sdk\cmdline-tools\latest\bin
```

Verify the setup in a new PowerShell window:

```powershell
$env:ANDROID_HOME
adb --version
```

### 6. Install Appium Globally

Install the Appium server through npm:

```powershell
npm install --global appium
```

Verify it:

```powershell
where.exe appium
appium --version
```

Because Appium is installed globally, do not install it again inside this Python project.

### 7. Install the UiAutomator2 Driver

Install Appium's Android automation driver:

```powershell
appium driver install uiautomator2
```

Verify the installed driver:

```powershell
appium driver list --installed
appium driver doctor uiautomator2
```

For a physical-device setup, warnings about the emulator can be ignored. Warnings about `bundletool`, FFmpeg, or GStreamer are optional unless the project needs Android App Bundles, screen recording, or screen streaming.

### 8. Install Appium Inspector (Optional)

Appium Inspector is used to view the current screen hierarchy and find element locators. It is not required to run existing tests.

Install the Inspector plugin:

```powershell
appium plugin install inspector
```

Verify it:

```powershell
appium plugin list --installed
```

Start Appium with the Inspector plugin:

```powershell
appium --address 127.0.0.1 --use-plugins=inspector --allow-cors
```

Use this server address in Inspector:

```text
http://127.0.0.1:4723
```

Example Inspector capabilities:

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:deviceName": "Android Device",
  "appium:udid": "<DEVICE_UDID>",
  "appium:appPackage": "<APP_PACKAGE>",
  "appium:appActivity": "<APP_ACTIVITY>",
  "appium:noReset": true
}
```

## Project Setup

Use these steps after cloning or copying the project to a computer that already has the machine-level dependencies installed.

### 1. Open the Project Directory

```powershell
cd "C:\path\to\appium-python-tests"
```

If the repository was cloned into a different location, use that location instead.

### 2. Create the Virtual Environment

Skip this command if `.venv` already exists and works:

```powershell
py -m venv .venv
```

Verify the virtual environment:

```powershell
Test-Path ".\.venv\Scripts\python.exe"
.\.venv\Scripts\python.exe --version
```

The first command should return `True`.

### 3. Install the Python Packages

Install the packages used by the tests:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install Appium-Python-Client pytest
```

Verify them:

```powershell
.\.venv\Scripts\python.exe -m pip show Appium-Python-Client
.\.venv\Scripts\python.exe -m pip show pytest
```

This project currently documents the required Python packages here instead of using a `requirements.txt` file.

## Prepare the Physical Android Device

### 1. Enable Developer Options

On the Android phone:

1. Open Settings.
2. Open About phone.
3. Tap Build number repeatedly until Developer Options are enabled.

The exact menu names can differ between Android manufacturers.

### 2. Enable USB Debugging

1. Open Developer Options.
2. Enable USB debugging.
3. Connect the phone to the computer using a data-capable USB cable.
4. Unlock the phone.
5. Accept the RSA debugging authorization prompt if it appears.

### 3. Verify the Device

Run:

```powershell
adb devices -l
```

Expected result:

```text
<DEVICE_UDID>    device
```

Use lowercase `-l`, not the number `-1`.

If the status is `unauthorized`, unlock the phone and accept the authorization prompt. If no device appears, try:

```powershell
adb kill-server
adb start-server
adb reconnect
adb devices -l
```

Also check the USB cable, USB connection mode, Windows device drivers, and whether the phone is unlocked.

## Run the Tests

Two PowerShell windows are normally required.

### Terminal 1: Start the Appium Server

For normal test execution:

```powershell
appium --address 127.0.0.1
```

Keep this terminal open while tests are running. The server should show that it is listening on `http://127.0.0.1:4723`.

When Appium Inspector is also required, start the server with:

```powershell
appium --address 127.0.0.1 --use-plugins=inspector --allow-cors
```

Do not start two Appium servers on port `4723` at the same time.

### Terminal 2: Run pytest

Open the project directory:

```powershell
cd "C:\path\to\appium-python-tests"
```

Run the complete test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s
```

Command meaning:

- `.\.venv\Scripts\python.exe` uses the project's Python environment.
- `-m pytest` starts pytest with that Python installation.
- `-v` displays each test name and result.
- `-s` displays `print()` output immediately.

Run one test file:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s .\tests\user_app\test_user_app_launch.py
```

Run one test function:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s ".\tests\user_app\test_user_app_launch.py::test_user_app_launch"
```

List discovered tests without running them:

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only
```

Stop the Appium server after testing by selecting its terminal and pressing `Ctrl+C`.

## Daily Test-Run Checklist

After completing the one-time setup, the normal routine is:

1. Connect and unlock the Android phone.
2. Confirm that USB debugging is enabled.
3. Verify the device with `adb devices -l`.
4. Start the Appium server in Terminal 1.
5. Run pytest in Terminal 2.

Commands:

```powershell
adb devices -l
appium --address 127.0.0.1
```

Then, in another PowerShell window:

```powershell
cd "C:\path\to\appium-python-tests"
.\.venv\Scripts\python.exe -m pytest -v -s
```

## Test-Writing Rules

Pytest automatically discovers:

- Files named `test_*.py` or `*_test.py`.
- Functions whose names begin with `test_`.

Example:

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

APP_PACKAGE = "replace-with-the-application-package"
APP_ACTIVITY = "replace-with-the-application-activity"


def test_application_launch():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "Android Device",
        "udid": "<DEVICE_UDID>",
        "appPackage": APP_PACKAGE,
        "appActivity": APP_ACTIVITY,
        "noReset": True,
        "forceAppLaunch": True,
    })

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options,
    )

    try:
        WebDriverWait(driver, 10).until(
            lambda current_driver:
                current_driver.current_package == APP_PACKAGE
        )

        assert driver.current_package == APP_PACKAGE

    finally:
        driver.quit()
```

Follow these rules when adding tests:

- Put test execution inside a function beginning with `test_`.
- Use assertions to verify the expected result.
- Use explicit waits instead of fixed `time.sleep()` calls where possible.
- Always close the Appium session using `driver.quit()` inside `finally` or a pytest fixture.
- Do not use `input()` because automated tests should not wait for manual terminal input.
- Do not treat a successful click as proof that the workflow passed; verify the resulting screen or state.
- Prefer stable locators such as Accessibility ID or Resource ID.
- Avoid relying on element instance numbers when a stable identifier is available.

## Organizing Tests in Subfolders

Creating subfolders inside `appium-python-tests` does not prevent pytest from finding the tests. Pytest searches through subfolders automatically when it is run from the repository root.

Recommended structure:

```text
appium-python-tests/
├── .gitignore
├── README.md
└── tests/
    ├── user_app/
    │   ├── test_user_app_launch.py
    │   └── test_user_app_login.py
    ├── driver_app/
    │   ├── test_driver_app_launch.py
    │   └── test_driver_app_login.py
    └── restaurant_app/
        ├── test_restaurant_app_launch.py
        └── test_restaurant_app_login.py
```

Follow these folder rules:

- Keep the virtual environment at the repository root, not inside `tests`.
- Use lowercase folder names with underscores and avoid spaces.
- Keep every test filename in the `test_*.py` format.
- Keep every test function name in the `test_*` format.
- Use unique filenames across the folders, such as `test_user_app_login.py` and `test_driver_app_login.py`.
- Run pytest from the `appium-python-tests` root so it can discover the complete suite.

Run every application test:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s .\tests
```

Run only one application folder:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s .\tests\driver_app
```

Run one test file:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s .\tests\driver_app\test_driver_app_login.py
```

Simple subfolders do not require `__init__.py`. If different folders contain files with exactly the same name, imports can become confusing; unique test filenames are the simplest way to avoid that problem.

## Finding an Application Package and Activity

Every HalalEats application has its own package and launch activity. Start the required application manually, then inspect the application currently in the foreground:

```powershell
adb shell dumpsys window | Select-String "mCurrentFocus|mFocusedApp"
```

The output normally contains a value resembling:

```text
com.example.application/.MainActivity
```

The text before `/` is the package, and the text after `/` is the activity.



## Git Repository Setup

The following generated or machine-specific directories should not be committed:

```gitignore
.venv/
.idea/
.vscode/
node_modules/
__pycache__/
.pytest_cache/
*.pyc
.env
credentials.py
reports/
screenshots/
recordings/
```

Initialize and commit the project:

```powershell
git init -b main
git status
git add .
git status
git commit -m "Initial Appium Python test setup"
```

Connect an empty GitHub repository and push it:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Review `git status` before every commit to make sure credentials, `.venv`, `.idea`, and generated files are not included.

## Project Directory Guidance

Keep these items in the repository:

```text
appium-python-tests/
├── .gitignore
├── README.md
└── tests/
    ├── user_app/
    ├── driver_app/
    └── restaurant_app/
```

These items may exist locally but should not be pushed:

```text
.venv/
.idea/
node_modules/
credentials.py
__pycache__/
.pytest_cache/
```

Do not delete `C:\Users\<WINDOWS_USERNAME>\.appium\node_modules`, because Appium drivers and plugins may be stored there. A `node_modules` directory located directly inside this Python project is unnecessary when Appium is installed globally.


## Scope Notes

- The Android Emulator is optional and is not required for the current physical-device workflow.
- `bundletool`, FFmpeg, and GStreamer are optional unless their related functionality is needed.
- Appium Inspector is a locator-development tool, not the test runner.
- The Appium server must remain running while the tests execute.
- The application must already be installed when only `appPackage` and `appActivity` are provided.
