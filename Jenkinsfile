pipeline {
    agent any
    
    stages {
        stage('Запуск OpenBMC') {
            steps {
                sh '''
                    chmod +x scripts/start_qemu.sh
                    ./scripts/start_qemu.sh
                    sleep 60
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
                    archiveArtifacts artifacts: 'reports/webui-tests.xml', allowEmptyArchive: true
                    junit 'reports/webui-tests.xml'
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
                    archiveArtifacts artifacts: 'reports/autotests.xml', allowEmptyArchive: true
                    junit 'reports/autotests.xml'
                }
            }
        }

        stage('Нагрузочное тестирование') {
            steps {
                sh ''' 
                    chmod +x scripts/run_locust.sh
                    ./scripts/run_locust.sh
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab6/locust-report.html', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'lab6/locust.log', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker stop qemu-openbmc || true && docker rm qemu-openbmc || true'
            archiveArtifacts artifacts: '**/*.html', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/*.xml', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
        }
    }
}