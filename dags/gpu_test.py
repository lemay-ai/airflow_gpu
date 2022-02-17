# gpu_test.py
# A simple Airflow DAG to check GPU availability.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.decorators import task
from airflow.utils.edgemodifier import Label

# Docker library from PIP
import docker

# Simple DAG
with DAG(
    "gpu_test", 
    schedule_interval="@daily", 
    start_date=datetime(2022, 1, 1), 
    catchup=False, 
    tags=['test']
) as dag:


    @task(task_id='check_gpu')
    def start_gpu_container(**kwargs):

         # get the docker params from the environment
         client = docker.from_env()
          
         # run the container
         response = client.containers.run(

             # The container you wish to call
             'tensorflow/tensorflow:2.7.0-gpu',

             # The command to run inside the container
             'nvidia-smi',

             # Passing the GPU access
             device_requests=[
                 docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
             ]
         )

         return str(response)

    check_gpu = start_gpu_container()


    # Dummy functions
    start = DummyOperator(task_id='start')
    end   = DummyOperator(task_id='end')


    # Create a simple workflow
    start >> check_gpu >> end
