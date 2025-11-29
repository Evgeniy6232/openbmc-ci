pipeline {
    agent any
    
    stages {
        stage('Запуск OpenBMC') {
            steps {
                sh '''
                    chmod +x scripts/start_qemu.sh
                    ./scripts/start_qemu.sh
                    sleep 90
                '''
            }
        }
        
        stage('WEB UI тесты') {
            steps {
                sh '''
                    chmod +x scripts/run_webui_tests.sh
                    ./scripts/run_webui_tests.sh
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab4/test-report.html', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker stop qemu-openbmc || true && docker rm qemu-openbmc || true'
        }
    }
}
