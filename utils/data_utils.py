# import pandas as pd
# import io

# def summarize_dataframe(df: pd.DataFrame) -> str:
#     """Generate a statistical + structural summary of the dataframe."""
#     buffer = io.StringIO()
#     buffer.write("Columns:\n")
#     buffer.write(", ".join(df.columns) + "\n\n")
#     buffer.write("Data types:\n")
#     buffer.write(str(df.dtypes) + "\n\n")
#     buffer.write("Summary statistics:\n")
#     buffer.write(str(df.describe(include='all')))
#     return buffer.getvalue()

# import pandas as pd
# import io

# def summarize_dataframe(df: pd.DataFrame) -> str:
#     """Generate a statistical + structural summary of the dataframe."""
#     buffer = io.StringIO()
#     buffer.write("Columns:\n")
#     buffer.write(", ".join(df.columns) + "\n\n")
#     buffer.write("Data types:\n")
#     buffer.write(str(df.dtypes) + "\n\n")
#     buffer.write("Summary statistics:\n")
#     buffer.write(str(df.describe(include='all')))
#     return buffer.getvalue()


import pandas as pd
import io

def summarize_dataframe(df: pd.DataFrame) -> str:
    buffer = io.StringIO()
    buffer.write('Columns:\n')
    buffer.write(', '.join(df.columns.astype(str)) + "\n\n")
    buffer.write('Sample (first 5 rows):\n')
    buffer.write(df.head(5).to_csv(index=False))
    buffer.write('\nData types:\n')
    buffer.write(str(df.dtypes) + "\n\n")
    buffer.write('Summary statistics:\n')
    try:
        buffer.write(str(df.describe(include='all')))
    except Exception:
        buffer.write('Describe failed for dataset')
    return buffer.getvalue()