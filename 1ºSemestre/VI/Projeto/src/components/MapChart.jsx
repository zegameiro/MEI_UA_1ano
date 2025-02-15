/* eslint-disable react/prop-types */
import { useEffect } from "react";
import countries from "../../public/data/countries.json";
import * as d3 from "d3";
import HelpPopHover from "./HelpPopOver";

const MapChart = ({ data, setCountry }) => {
  useEffect(() => {
    const countryData = new Set(data.map((d) => d.country));

    const handleCountryClick = (event, country) => {
      setCountry(country);
    };

    // Specify the chart’s dimensions.
    const width = 1000;
    const marginTop = 46;
    const height = width / 2 + marginTop;

    // Fit the projection.
    const projection = d3.geoEqualEarth().fitExtent(
      [
        [2, marginTop + 2],
        [width - 2, height],
      ],
      { type: "Sphere" }
    );
    const path = d3.geoPath(projection);

    const svg = d3
      .select("#map-chart")
      .html("")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

    const g = svg.append("g")

    const tooltip = d3
      .select("body")
      .append("div")
      .style("position", "absolute")
      .style("background", "black")
      .style("border", "1px solid #ccc")
      .style("padding", "8px")
      .style("border-radius", "4px")
      .style("box-shadow", "0px 2px 10px rgba(0, 0, 0, 0.1)")
      .style("visibility", "hidden")
      .style("pointer-events", "none")
      .style("font-size", "12px")
      .style("color", "white");

    g.append("path").attr("d", path);

    g.selectAll("path")
      .data(countries.features)
      .join("path")
      .attr("d", path)
      .attr("fill", (d) =>
        countryData.has(d.properties.name) ? "lightgreen" : "lightgray"
      )
      .attr("stroke", "gray")
      .style("cursor", (d) =>
        countryData.has(d.properties.name) ? "pointer" : "not-allowed"
      )
      .on("click", function (event, d) {
        if (countryData.has(d.properties.name))
          handleCountryClick(event, d.properties.name);
      })
      .on("mouseover", (event, d) => {
        tooltip
          .style("visibility", "visible")
          .html(d.properties.name)
          .style(
            "color",
            countryData.has(d.properties.name) ? "white" : "gray"
          );
      })
      .on("mousemove", (event) => {
        tooltip
          .style("top", `${event.pageY - 10}px`)
          .style("left", `${event.pageX + 10}px`);
      })
      .on("mouseout", () => {
        tooltip.style("visibility", "hidden");
      })
      .append("title")
      .text((d) => d.properties.name)
      .attr("fill", "white");

      const zoom = d3.zoom()
        .scaleExtent([1, 8])
        .on("zoom", (event) => {
          g.attr("transform", event.transform);
        });

      svg.call(zoom);

      return () => {
        tooltip.remove();
        svg.on(".zoom", null)
      };

  }, [data, setCountry]);

  const information = {
    "About this Visualization" : "This interactive map of the world displays the countries that have data about songs statistics in Spotify.",
    "Key Features": [
      "Countries that have the a light green color, means that it exists statistics about Spotify in this country, so you can select this country",
      "Countries that have a light gray color don't have any data and therefore you're not allowed to select it",
      "When you hover over a country with a light green color a tooltip displays with the name of the country",
      "Zoom in and zoom out in the map"
    ],
    "How to use": "Look for the country that you want to learn more about Spotify statistics associated, and if the country you want has a light green color than you can select it, otherwize you can't."
  };

  return (
    <div className="flex flex-col text-center">
      <div className="flex flex-row items-center justify-between">
        <h1 className="font-semibold text-lg">Map of the World</h1>
        <HelpPopHover information={information} placement="down" />
      </div>
      <svg id="map-chart"></svg>
    </div>
  );
};

export default MapChart;
