pipeline {
   agent {label 'docker'}

   stages {

      stage('cleanup') {
         steps {
            sh '''
            pwd
            for f in $(ls -A); do rm -rf ${f}; done
            '''
         }
      }

      stage('clone') {
         steps {
            sh 'git clone https://github.com/vitodb/decisionengine.git'
         }
      }

      stage('pull docker image') {
         steps {
            sh 'docker pull ${DOCKER_IMAGE}'
         }
      }

      stage('pylint') {
         steps {
            echo 'Run pylint tests'
            sh '''
            pwd
            docker run --rm -u 500:500 -v $PWD:$PWD -v ${WORKSPACE}:/workspace -w ${PWD} ${DOCKER_IMAGE} decisionengine/.github/actions/pylint-in-sl7-docker/entrypoint.sh
            '''
         }
      }

      stage('unit tests') {
         steps {
            echo 'Run pylint tests'
            sh '''
            pwd
            docker run --rm -u 500:500 -v $PWD:$PWD -v ${WORKSPACE}:/workspace -w ${PWD} ${DOCKER_IMAGE} decisionengine/.github/actions/unittest-in-sl7-docker/entrypoint.sh
            '''
         }
      }
      
   }
}
