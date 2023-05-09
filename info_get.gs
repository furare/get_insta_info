function formatDateToJapanTime(date) {
 const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Asia/Tokyo'
  };

  const formatter = new Intl.DateTimeFormat('ja-JP', options);
  const formattedDate = formatter.format(date);

  return formattedDate;
};

function doPost(e) {
  var prop = PropertiesService.getScriptProperties().getProperties();
  var ss = SpreadsheetApp.openById(prop.SheetID);
  var sheet = ss.getSheetByName("{YOUR SHEET NAME}");

  var data = JSON.parse(e.postData.contents);  

  var row = [formatDateToJapanTime(new Date()), data.follower, data.following];
  sheet.appendRow(row);

  var response = {
    status: "success",
    message: "OK"
  };

  return ContentService.createTextOutput(JSON.stringify(response)).setMimeType(ContentService.MimeType.JSON);
};