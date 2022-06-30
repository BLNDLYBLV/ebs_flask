const { getContinentGeoJSONByCode } = require("geojson-places");
const fs = require('fs')

// Get the continent geojson of Europe
const continents = {};
const continents_name = ['Europe','Asia','Africa','Antartica','North America','South America','Oceania'];
const continents_code = ['EU','AS','AF','AN','NA','SA','OC'];
for(var i = 0; i<continents_code.length; i++){
    const result = getContinentGeoJSONByCode(continents_code[i]);
    continents[continents_name[i]] = result;
}

const continentsJSON = JSON.stringify(continents);

fs.writeFile('continents.json',continentsJSON,(err)=>{if(err) console.log(e); else console.log('Saved succesfully')});