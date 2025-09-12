pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'patch-1', url: 'https://github.com/BS-Pranav/Timeless-Echoes-Main.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                bat '''
                python -m venv venv

                REM Ensure pip exists
                venv\\Scripts\\python.exe -m ensurepip --upgrade

                REM Upgrade pip and essentials
                venv\\Scripts\\python.exe -m pip install --upgrade pip setuptools wheel

                REM Install requirements if available
                if exist requirements.txt (
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                )

                REM Install pytest explicitly
                venv\\Scripts\\python.exe -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                set PYTHONUTF8=1
                venv\\Scripts\\python.exe -m pytest -s
                '''
            }
        }
    }
}
