pipeline{
	agent any
		stages{
			stage("checkout"){
				steps{
					checkout scm
				}
			}
			stage('build image'){
				steps{
					sh 'docker compose build'
				}
			}
			stage('Run Container'){
				steps{
					sh 'docker compose up -d'
				}
			}
		}
}
