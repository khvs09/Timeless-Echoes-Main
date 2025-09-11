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
                call venv\\Scripts\\activate
                python -m ensurepip --upgrade
                python -m pip install --upgrade pip setuptools wheel
                if exist requirements.txt (
                    python -m pip install -r requirements.txt
                )
                python -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                set PYTHONUTF8=1
                python -m pytest -s
                '''
            }
        }
    }
}
