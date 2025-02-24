"""
Contains the main `FastAPI_Wrapper` class, which wraps `FastAPI`.
"""
import os


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

CORS_ALLOW_ORIGINS=['http://localhost, http://localhost:4010, http://localhost:8765, http://localhost:8502'] # http://jedscene-env.eba-qrbhqiku.us-east-2.elasticbeanstalk.com/

class FastAPI_Wrapper(FastAPI):

    def __init__(self):
        """
        Initializes a FastAPI instance to run a LRP.
        """
        print('Initializing FastAPI_Wrapper...')
        
        super().__init__()

        origins = CORS_ALLOW_ORIGINS

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Add shutdown event (would only be of any use in a multi-process, not multi-thread situation)
        @self.get("/shutdown")
        async def shutdown():
            import time
            import psutil
            import threading

            def suicide():
                time.sleep(1)
                myself = psutil.Process(os.getpid())
                myself.kill()

            threading.Thread(target=suicide, daemon=True).start()
            print(f'>>> Successfully killed API <<<')
            return {"success": True}  

        @self.get("/run")
        async def run():
            import time
            from datetime import datetime
            import threading

            # !! RUN YOUR LONG-RUNNING PROCESS HERE !!
            def lrp_runner():
                while True:
                    time.sleep(10)
                    print(f'>>> LRP Report @ {datetime.now()} <<<')

            threading.Thread(target=lrp_runner, daemon=True).start()

