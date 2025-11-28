pipeline {
    agent {
        docker {
            image 'qemuorg/qemu:latest'
            args '--privileged --network host'
        }
    }
    
    stages {
        stage('Запуск OpenBMC') {
            steps {
                sh '''
                    echo "Запуск OpenBMC в QEMU"
                    mkdir -p romulus
                    cp /var/openbmc-images/obmc-phosphor-image-romulus-20250909100209.static.mtd ./romulus/
                    echo "Файл образа скопирован успешно"
                    echo "QEMU не установлен, пропускаем запуск"
                '''
            }
        }
        
        stage('Run OpenBMC Auto Tests (pytest)') {
            steps {
                sh '''
                    echo "=== ЗАПУСК АВТОТЕСТОВ OPENBMC (PYTEST) ==="
                    
                    # Запуск реальных API тестов из lab5
                    cd lab4/openbmc_tests
                    source ../../venv/bin/activate
                    python -m pytest lab5.py -v --html=../../test-results/api-tests.html
                    
                    echo "Автотесты завершены"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test-results/api-tests.html', fingerprint: true
                    publishHTML target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'test-results',
                        reportFiles: 'api-tests.html',
                        reportName: 'API Test Report'
                    ]
                }   
            }
        }
        
        stage('WebUI Тесты') {
            steps {
                sh '''
                    echo "=== ЗАПУСК WEBUI ТЕСТОВ OPENBMC ==="
                    
                    # Запуск реальных WebUI тестов из lab4
                    cd lab4/openbmc_tests
                    source ../../venv/bin/activate
                    
                    # Запуск Selenium тестов
                    for test_file in test_ban.py test_error.py test_login.py test_OnOff.py test_temp.py; do
                        if [ -f "$test_file" ]; then
                            echo "Запуск теста: $test_file"
                            python "$test_file"
                        fi
                    done
                    
                    # Создаем отчет
                    echo "WebUI тесты завершены" > webtest-report.html
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'webtest-report.html', fingerprint: true
                    publishHTML target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'webtest-report.html',
                        reportName: 'WebUI Test Report'
                    ]
                }
            }
        }
        
        stage('Нагрузочное тестирование') {
            steps {
                sh '''
                    echo "=== НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ ==="
                    
                    # Запуск Locust тестов из lab6
                    cd lab6
                    source ../venv/bin/activate
                    locust -f load_test.py --headless -u 10 -r 1 -t 30s --html=../test-results/loadtest.html
                    
                    echo "Нагрузочное тестирование завершено" > loadtest.jtl
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'loadtest.jtl,test-results/loadtest.html', fingerprint: true
                    publishHTML target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'test-results',
                        reportFiles: 'loadtest.html',
                        reportName: 'Load Test Report'
                    ]
                }
            }
        }
    }
    
    post {
        always {
            sh '''
                echo "Пайплайн завершён"
            '''
        }
    }
}