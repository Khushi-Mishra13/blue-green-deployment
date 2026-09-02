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
                        stage('Health check green'){
				steps{
					sh 'docker compose exec nginx wget -qO- http://green:5000/health'
				}
			}
			stage('Switch containers'){
				steps{
					sh '''
						docker compose exec green nginx -s reload
					'''
				 }
			}
		}

		post{
			success{
				echo 'Green deployment successful'
			}
			failure{
				echo 'Deployment failed'
			}
		}
}
