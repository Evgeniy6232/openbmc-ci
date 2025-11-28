pipeline {
    agent any
    
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
                    cd lab4/openbmc_tests
                    echo "Запуск теста: lab5.py"
                    python lab5.py
                    echo "Автотесты завершены"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab4/openbmc_tests/lab5.py', fingerprint: true
                }   
            }
        }
        
        stage('WebUI Тесты') {
            steps {
                sh '''
                    echo "=== ЗАПУСК WEBUI ТЕСТОВ OPENBMC ==="
                    cd lab4/openbmc_tests
                    echo "Запуск WebUI тестов..."
                    for test_file in test_ban.py test_error.py test_login.py test_OnOff.py test_temp.py; do
                        if [ -f "$test_file" ]; then
                            echo "Запуск теста: $test_file"
                            python "$test_file"
                        fi
                    done
                    echo "WebUI тесты завершены"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab4/openbmc_tests/test_*.py', fingerprint: true
                }
            }
        }

        stage('Нагрузочное тестирование') {
            steps {
                sh '''
                    echo "=== НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ ==="
                    cd lab6
                    echo "Запуск Locust теста..."
                    python locusfile.py
                    echo "Нагрузочное тестирование завершено"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab6/locusfile.py', fingerprint: true
                }    
            }
         }
    }
    
    post {
        always {
            sh '''
                echo "🎉 Пайплайн завершён!"
            '''
        }
    }
}