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
			stage('Testing SSH Connection'){
				steps{
					sshagent(credentials: ['khushi-vm']) {
						sh '''
						    [ -d ~/.ssh ] || mkdir ~/.ssh && chmod 0700 ~/.ssh
						    ssh -p 5125 khushi@192.168.7.102
					  '''
					}
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
						 docker compose exec -T nginx nginx -s reload
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
