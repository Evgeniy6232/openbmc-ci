pipeline {
    agent any
    
    stages {                   
        stage('Запуск OpenBmc') {
            steps {
                sh '''
                    chmod +x ./scripts/start_qemu.sh
                    ./scripts/start_qemu.sh &
                    sleep 60
                '''
         stage('WEB UI тесты') {
            steps {
                sh '''
                    source lab4/venv/bin/activate

                    ls -la lab4/openbmc_tests/*.py
                    
                    pytest lab4/openbmc_tests/ \
                        --html=lab4/test-report.html \
                        --self-contained-html \
                        -v \
                        --tb=short
                    
                    echo "WEB UI тесты завершены!"
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'lab4/',
                        reportFiles: 'test-report.html',
                        reportName: 'OpenBMC WEB UI Test Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            sh '''
                docker stop qemu-openbmc || true
                docker rm qemu-openbmc || true
            '''
            echo 'Очистка завершена'
        }
    }
}
