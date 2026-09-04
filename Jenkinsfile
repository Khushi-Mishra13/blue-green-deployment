def remote = [:]
remote.name = "khushi-vm"
remote.user = "khushi"
remote.host = "192.168.7.102"
remote.port - '5125'
remote.allowAnyHosts = true

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
					/*withCredentials([sshUserPrivateKey(credentialsId: 'khushi-vm', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'khushi')]) {
        			remote.user = khushi
        			remote.identityFile = identity
        			stage("SSH Steps Rocks!")
					sh 'docker compose build' */
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
			        // Nest withCredentials inside sshagent (or vice-versa), removing the comma
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
