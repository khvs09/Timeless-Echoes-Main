pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/khvs09/Timeless-Echoes-Main.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate

                REM Ensure pip is available
                python -m ensurepip --upgrade

                REM Upgrade pip and essentials
                python -m pip install --upgrade pip setuptools wheel

                REM Install requirements if available
                if exist requirements.txt (
                    python -m pip install -r requirements.txt
                )

                REM Install pytest explicitly
                python -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python -m pytest
                '''
            }
        }
    }
}
