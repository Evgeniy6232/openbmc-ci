pipeline {
    agent any
    
    stages {
        stage('Запуск OpenBMC') {
            steps {
                sh '''
                    chmod +x scripts/start_qemu.sh
                    ./scripts/start_qemu.sh
                    sleep 180
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
        
        stage('Автотесты') {
            steps {
                sh '''
                    chmod +x scripts/run_autotests.sh
                    ./scripts/run_autotests.sh
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab4/test-report.html', allowEmptyArchive: true
                    junit 'reports/autotests.xml'
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
