pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'patch-1',
                    url: 'https://github.com/BS-Pranav/Timeless-Echoes-Main.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                bat '''
                REM Create virtual environment
                python -m venv venv

                REM Download get-pip.py to fix broken pip
                curl -sSLo get-pip.py https://bootstrap.pypa.io/get-pip.py

                REM Install pip into the venv
                venv\\Scripts\\python.exe get-pip.py

                REM Upgrade pip, setuptools, wheel
                venv\\Scripts\\python.exe -m pip install --upgrade pip setuptools wheel

                REM Install project requirements if present
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
                REM Run pytest with unbuffered output so console shows print() statements
                venv\\Scripts\\python.exe -u -m pytest -s -v
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '✅ Tests passed successfully!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
