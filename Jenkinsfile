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

                REM Ensure pip exists
                venv\\Scripts\\python.exe -m ensurepip --upgrade

                REM Force reinstall pip, setuptools, wheel to fix broken pip
                venv\\Scripts\\python.exe -m pip install --upgrade --force-reinstall pip setuptools wheel

                REM Install requirements if available
                if exist requirements.txt (
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                )

                REM Ensure pytest is installed
                venv\\Scripts\\python.exe -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                venv\\Scripts\\pytest
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
