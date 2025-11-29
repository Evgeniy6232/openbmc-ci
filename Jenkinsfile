pipeline {
    agent any
    options {
        skipDefaultCheckout()
    }
    
    stage('Запуск OpenBmc') {
        steps {
            sh '''
                chmod +x ./scripts/start_qemu.sh
                ./scripts/start_qemu.sh &
                sleep 60
            '''
        }
    }
}
