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
                python -m ensurepip --upgrade
                python -m pip install --upgrade pip
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
                python -m pytest -s
                '''
            }
        }
    }
}
