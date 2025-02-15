import { useState, useEffect } from "react";
import { Button } from "@nextui-org/react";
import * as d3 from "d3";

import MapChart from "../components/MapChart";
import Top10 from "../components/Top10";
import LineChart from "../components/LineChart";
import PieChart from "../components/PieChart";
import BarChart from "../components/BarChart";
import BubbleMap from "../components/BubbleMap";
import CompareModal from "../components/CompareModal";
import NavBarComp from "../components/NavBarComp";

const MainPage = () => {
  const [data, setData] = useState([]);
  const [country, setCountry] = useState("");
  const [countryData, setCountryData] = useState([]);
  const [song, setSong] = useState();

  useEffect(() => {
    // fetch csv
    const fetchData = async () => {
      const response = await fetch("/data/reduced_file.csv");
      const data = await response.text();
      const parsedData = d3.csvParse(data);
      setData(parsedData);
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (data.length > 0) {
      const d = data.filter((d) => {
        if (country !== "") return d.country === country;

        return d.country === "";
      });
      setCountryData(d);
    }
  }, [data, country, setCountryData]);

  return (
    <div className="flex flex-col">
      <NavBarComp />
      <div className="flex flex-col min-h-screen px-10 py-5">
        {data.length > 0 && (
          <div className="flex flex-col">
            <div className="flex flex-row justify-between">
              {song != null ? (
                <BubbleMap data={data} song={song} setCountry={setCountry} />
              ) : (
                <MapChart data={data} setCountry={setCountry} />
              )}
              <Top10
                data={countryData.slice(0, 10)}
                country={country}
                setSong={setSong}
                song={song}
              />
            </div>
            <div className="flex flex-row py-10 space-x-5">
              <Button
                color="primary"
                onClick={() => {
                  setCountry("");
                  setSong(null);
                }}
              >
                Clear Filters
              </Button>
              <CompareModal data={data} country={country} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <LineChart data={data} country={country} />
              <PieChart data={data} country={country} />
              <BarChart data={data} country={country} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MainPage;
