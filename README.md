# Task HRMS - ERPNext Leave & Attendance Module

## Project Overview

This repository (`task_hrms`) implements a **Leave & Attendance approval workflow** within the ERPNext framework. The project is designed to demonstrate full-stack development capabilities, including custom Doctypes, server-side validations, client-side scripting, workflow logic, and reporting. The module provides functionality for managing leave requests, approving them, and generating summary reports by employee.

## Features

- **Custom Doctype**: Leave Request with fields for Employee, From Date, To Date, Leave Type, Status, and Approved By.
- **Server-side Validation**:

  - Ensures leave duration does not exceed 5 days.
  - Validates that `From Date` is before `To Date`.

- **Workflow & Approval**:

  - Custom "Approve" button visible only to HR Managers for pending leave requests.
  - Updates `Status` to "Approved" and sets the `Approved By` field to the current user.

- **Client-side Scripting**:

  - Displays a message for "Earned Leave (EL)" selection: "Earned Leave requires manager approval."
  - Automatically calculates total leave days (excluding weekends) in a read-only `Total Days` field.

- **Script Report**: Leave Summary by Employee showing Total Leave Requests, Approved Leaves, and Rejected Leaves, grouped by Employee.

### Docker Setup

1.  Setup folder and download the required files:

    ```bash
    mkdir task_hrms
    cd task_hrms

    # Download the docker-compose file
    wget -O docker-compose.yml https://raw.githubusercontent.com/sohan653/task_hrms/invento/docker/docker-compose.yaml

    # Download the setup script
    wget -O init.sh https://raw.githubusercontent.com/sohan653/task_hrms/invento/docker/init.sh
    ```

2.  Run the container and daemonize it:

    ```bash
    docker compose up
    ```

3.  After all process completed then access the instance at `http://localhost:8000` with credentials:
    - **Username**: Administrator
    - **Password**: admin

## Local Setup

To setup the repository locally, follow the steps mentioned below:

### 1. Install Frappe Bench

Install bench version 15 and setup a `frappe-bench` directory by following the [Installation Steps](https://frappeframework.com/docs/user/en/installation)

### 2. Start the Server

Start the server by running:

```bash
bench start
```

### 3. Create New Site

In a separate terminal window, create a new site by running:

```bash
bench new-site hr.localhost
```

### 4. Map Site to Localhost

Map your site to localhost with the command:

```bash
bench --site hr.localhost add-to-hosts
```

### 5. Get App

Get the Erpnext & Hrms app by running:

```bash
bench get-app --branch version-15 erpnext
bench get-app https://github.com/sohan653/task_hrms
```

### 6. Install the App

Run the following command to install the app:

```bash
bench --site hr.localhost install-app erpnext
bench --site hr.localhost install-app task_hrms

```

### 7.Set bench developer mode on the new site

```
bench --site hr.localhost set-config developer_mode 1
bench --site hr.localhost clear-cache
```

### 8. Access the Application

Now open the URL `http://hr.localhost:8000` in your browser. You should see the app running.

## Learn and Connect

## Default Credentials

- **Username**: Administrator
- **Password**: admin

## Usage

### Creating a Leave Request:

1. Navigate to the **Leave Request** module in ERPNext.
2. Fill in `Employee`, `From Date`, `To Date`, `Leave Type`, and `Status` (defaults to "Pending").
3. The system enforces validations for leave duration and date order.

### Approving a Leave Request:

1. HR Managers will see an "Approve" button on pending leave requests.
2. Clicking it sets `Status` to "Approved" and records the current user as the Approver.

### Dynamic Behaviors:

- Selecting **"EL"** triggers a message: "Earned Leave requires manager approval."
- Changing `From Date` or `To Date` updates the `Total Days` field (excluding weekends).

### Viewing the Report:

1. Access the **Leave Summary by Employee** report from the ERPNext report menu.
2. View aggregated data for Total Leave Requests, Approved Leaves, and Rejected Leaves.
