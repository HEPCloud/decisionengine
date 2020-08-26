pipeline {
    agent { label 'docker' }
    stages{
        stage('DE tests') {
            parallel {
                stage('pylint') {
                    agent {
                        node {
                            label 'docker'
                            customWorkspace "${WORKSPACE}/${STAGE_NAME}"
                        }
                    }
                    steps {
                        script {
                            // DOCKER_IMAGE is defined through Jenkins project
                            pylintStageDockerImage="${DOCKER_IMAGE}_${BUILD_NUMBER}_${STAGE_NAME}"
                            // Set custom Build Name
                            if (params.GITHUB_PR_NUMBER) {
                                currentBuild.displayName="${BUILD_NUMBER}#PR#${GITHUB_PR_NUMBER}"
                            } else {
                                currentBuild.displayName="${BUILD_NUMBER}#${BRANCH}"
                            }
                        }
                        echo "cleanup workspace"
                        sh 'for f in $(ls -A); do rm -rf ${f}; done'
                        // DE_REPO is defined through Jenkins project
                        echo "clone decisionengine code from ${DE_REPO}"
                        sh '''
                            git clone ${DE_REPO}
                            echo GITHUB_PR_NUMBER: ${GITHUB_PR_NUMBER}
                            if [[ -n ${GITHUB_PR_NUMBER} ]]; then
                                cd decisionengine
                                git fetch origin pull/${GITHUB_PR_NUMBER}/merge:merge${GITHUB_PR_NUMBER}
                                git checkout merge${GITHUB_PR_NUMBER}
                                cd ..
                            fi
                        '''
                        echo "prepare docker image ${pylintStageDockerImage}"
                        sh "docker build -t ${pylintStageDockerImage} -f decisionengine/.github/actions/pylint-in-sl7-docker/Dockerfile.jenkins decisionengine/.github/actions/pylint-in-sl7-docker/"
                        echo "Run ${STAGE_NAME} tests"
                        sh "docker run --rm -v ${WORKSPACE}:${WORKSPACE} -w ${WORKSPACE} ${pylintStageDockerImage}"
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: "pep8.master.log,pylint.master.log,results.master.log,mail.results"
                            echo "cleanup docker image ${pylintStageDockerImage}"
                            sh "docker rmi ${pylintStageDockerImage}"
                        }
                    }
                }
                stage('unit_tests') {
                    agent {
                        node {
                            label 'docker'
                            customWorkspace "${WORKSPACE}/${STAGE_NAME}"
                        }
                    }
                    steps {
                        script {
                            // DOCKER_IMAGE is defined through Jenkins project
                            unit_testsStageDockerImage="${DOCKER_IMAGE}_${BUILD_NUMBER}_${STAGE_NAME}"
                        }
                        echo "cleanup workspace"
                        sh 'for f in $(ls -A); do rm -rf ${f}; done'
                        // DE_REPO is defined through Jenkins project
                        echo "clone decisionengine code from ${DE_REPO}"
                        sh '''
                            git clone ${DE_REPO}
                            echo GITHUB_PR_NUMBER: ${GITHUB_PR_NUMBER}
                            if [[ -n ${GITHUB_PR_NUMBER} ]]; then
                                cd decisionengine
                                git fetch origin pull/${GITHUB_PR_NUMBER}/merge:merge${GITHUB_PR_NUMBER}
                                git checkout merge${GITHUB_PR_NUMBER}
                                cd ..
                            fi
                        '''
                        echo "prepare docker image ${unit_testsStageDockerImage}"
                        sh "docker build -t ${unit_testsStageDockerImage} -f decisionengine/.github/actions/unittest-in-sl7-docker/Dockerfile.jenkins decisionengine/.github/actions/unittest-in-sl7-docker"
                        echo "Run ${STAGE_NAME} tests"
                        sh "docker run --rm -v ${WORKSPACE}:${WORKSPACE} -w ${WORKSPACE} ${unit_testsStageDockerImage}"
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: "pytest.log"
                            echo "cleanup docker image ${unit_testsStageDockerImage}"
                            sh "docker rmi ${unit_testsStageDockerImage}"
                            }
                    }
                }
                stage('rpmbuild') {
                    agent {
                        node {
                            label 'docker'
                            customWorkspace "${WORKSPACE}/${STAGE_NAME}"
                        }
                    }
                    steps {
                        script {
                            // DOCKER_IMAGE is defined through Jenkins project
                            rpmbuildStageDockerImage="${DOCKER_IMAGE}_${BUILD_NUMBER}_${STAGE_NAME}"
                        }
                        echo "cleanup workspace"
                        sh 'for f in $(ls -A); do rm -rf ${f}; done'
                        // DE_REPO is defined through Jenkins project
                        echo "clone decisionengine code from ${DE_REPO}"
                        sh '''
                            git clone ${DE_REPO}
                            echo GITHUB_PR_NUMBER: ${GITHUB_PR_NUMBER}
                            if [[ -n ${GITHUB_PR_NUMBER} ]]; then
                                cd decisionengine
                                git fetch origin pull/${GITHUB_PR_NUMBER}/merge:merge${GITHUB_PR_NUMBER}
                                git checkout merge${GITHUB_PR_NUMBER}
                                cd ..
                            fi
                        '''
                        echo "prepare docker image ${rpmbuildStageDockerImage}"
                        sh "docker build -t ${rpmbuildStageDockerImage} -f decisionengine/.github/actions/rpmbuild-in-sl7-docker/Dockerfile.jenkins decisionengine/.github/actions/rpmbuild-in-sl7-docker"
                        echo "Run ${STAGE_NAME} tests"
                        sh "docker run --rm -v ${WORKSPACE}:${WORKSPACE} -w ${WORKSPACE} ${rpmbuildStageDockerImage}"
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: "rpmbuild.tar"
                            echo "cleanup docker image ${rpmbuildStageDockerImage}"
                            sh "docker rmi ${rpmbuildStageDockerImage}"
                        }
                    }
                }
            }
        }
    }
}
