from fastapi import FastAPI
from router.upload_file_router import router as upload_file_router
from router.print_job_router import router as print_job_router
from router.printers_router import router as printer_router
from router.user_route import router as user_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.include_router(upload_file_router, tags=['Upload File'])
app.include_router(print_job_router, tags=['Print Job'])
app.include_router(printer_router, tags=['Printers'])
app.include_router(user_router, tags=['User'])

app.add_middleware(
    CORSMiddleware,
    # Replace '*' with the specific origin if needed
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
