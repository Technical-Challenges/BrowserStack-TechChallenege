pipeline {
   agent any
   stages {
      stage('setup') {
         steps {
            browserstack(credentialsId: 'c567963d-060b-4e14-bdba-b6921312361b') {
               echo "TEST"
               sh browserstack-sdk pytest -s .\tests\test_browserstack.py
            }
            browserStackReportPublisher 'automate'
         }
      }
    }
  }
