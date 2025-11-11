// Small script to download the OMOP table as a TSV
// Make sure to show all records, then run this in the browser console and you'll download the table.

function table_to_array(table) {
  let rows = table.getElementsByTagName('tr');
  let table_data = []
  for (let i = 0; i < rows.length; i++) {
    let row_data = []
    let cols = rows[i].querySelectorAll('td,th');
    for (let j = 0; j < cols.length; j++) {
      row_data.push(cols[j].innerText)
    }
    table_data.push(row_data)
  }
  return(table_data)
}

function table_array_to_str(data, datum_sep = '\t', row_sep='\n') {
  for (let i = 0; i < data.length; i++) {
    // Remove illegal characters:
    data[i] = data[i].map(x => x.replace(datum_sep, "").replace(row_sep, ""))
    data[i] = data[i].join(datum_sep);
  }
  return(data.join(row_sep))
}

function download_str_to_file(str, extension = 'tsv') {
  let data = new Blob([str], {type: 'text/' + extension});
  let link = document.createElement('a');
  link.download = 'data.' + extension;
  let url = window.URL.createObjectURL(data);
  link.href = url;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

let omop_table = document.querySelector('table')
download_str_to_file(table_array_to_str(table_to_array(omop_table)))