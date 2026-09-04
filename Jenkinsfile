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
					sh 'docker build -t ghcr.io/khushi-mishra13/blue-green-deployment:latest .'
				}
			}

			stage('push it to ghcr'){
			    steps {
			        withCredentials([
			            usernamePassword(
			                credentialsId: 'github-token-id',
			                usernameVariable: 'username',
			                passwordVariable: 'password' 
			            )
			        ]) {
			        sh '''
			            echo "$password" | docker login ghcr.io -u "$username" --password-stdin
			            docker push ghcr.io/khushi-mishra13/blue-green-deployment:latest
			        '''
					}
			    }
			}
			
			stage('Deploying On VM'){
				steps {
			        sshagent(credentials: ['khushi-vm']) {
			            withCredentials([
			                usernamePassword(
			                    credentialsId: 'github-token-id',
			                    usernameVariable: 'username',
			                    passwordVariable: 'password'
			                )
			            ]) {
							sh '''
								ssh -o StrictHostKeyChecking=no -p 5125 khushi@192.168.7.102 << EOF
									echo "$password" | docker login ghcr.io -u "$username" --password-stdin
									
									# Stop and remove existing container if it exists to avoid port conflicts
									docker rm -f blue-app || true
									
									docker pull ghcr.io/khushi-mishra13/blue-green-deployment:latest
									docker run -d --name blue-app -p 8081:5000 ghcr.io/khushi-mishra13/blue-green-deployment:latest
								EOF
						'''
						}
					}
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
