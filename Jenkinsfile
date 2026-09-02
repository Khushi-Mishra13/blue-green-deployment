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
						sed -i 's|proxy_pass http://blue:5000|proxy_pass http://green:5000|' nginx/nginx.conf
						docker exec 55fa29eb531e nginx -s reload
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
