from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
import pandas as pd
from .models import Shop

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                # Load the Excel file into a DataFrame
                df = pd.read_excel(excel_file, header=None)
                
                # Find the header row index by checking if any cell contains 'place_name'
                header_row_index = None
                for idx, row in df.iterrows():
                    if row.str.contains('place_name', case=False).any():
                        header_row_index = idx
                        break

                # If header row index is found, re-read the Excel file with proper header row
                if header_row_index is not None:
                    df = pd.read_excel(excel_file, header=header_row_index)
                    # Now, df contains data with correct header row

                    # Iterate over the DataFrame rows and save each row to the database
                    for index, row in df.iterrows():
                        shop = Shop.objects.create(
                            serving=row['serving'],
                            place_name=row['place_name'],
                            phone_number=row['phone_number'],
                            work_time=row['work_time'],
                            locations=row['locations'],
                            services=row['services'],
                            serving_car_type=row['serving_car_type'],
                            image_urls=row['image_urls'],
                            long_lat=row['long_lat']
                        )
                    return redirect('upload_success')  # Redirect to success page
                else:
                    raise Exception("Header row not found in Excel file.")
            except Exception as e:
                # Handle exceptions and provide feedback to the user
                return render(request, 'upload_excel.html', {'form': form, 'error': str(e)})
    else:
        form = ExcelUploadForm()
    return render(request, 'upload_excel.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')





