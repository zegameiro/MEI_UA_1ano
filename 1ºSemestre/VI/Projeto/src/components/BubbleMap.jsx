import { useEffect } from "react";
import countries from "../../public/data/countries.json";
import * as d3 from "d3";

import HelpPopHover from "./HelpPopOver";

const BubbleMap = ({ data, song, setCountry }) => {
  useEffect(() => {
    const songDataByCountry = data.filter(
      (s) => s.spotify_id === song.spotify_id && s.country !== ""
    );

    const countryData = new Set(data.map((d) => d.country));

    const width = 1000;
    const marginTop = 46;
    const height = width / 2 + marginTop;

    const projection = d3.geoEqualEarth().fitExtent(
      [
        [2, marginTop + 2],
        [width - 2, height],
      ],
      { type: "Sphere" }
    );

    const path = d3.geoPath(projection);

    const svg = d3
      .select("#bubble-map")
      .html("")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

    svg.selectAll("*").remove();

    const g = svg.append("g");

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

    g.append("g")
      .selectAll("path")
      .data(countries.features)
      .join("path")
      .attr("d", path)
      .attr("fill", (d) =>
        countryData.has(d.properties.name) ? "lightgreen" : "lightgray"
      )
      .attr("stroke", "gray")
      .style("cursor", (d) =>
        countryData.has(d.properties.name) ? "default" : "not-allowed"
      );

    const maxPopularity = d3.max(songDataByCountry, (d) => d.daily_rank) || 1;

    const bubbleScale = d3.scaleSqrt().domain([0, maxPopularity]).range([0, 3]);

    // Scale for bubble color
    const colorScale = d3
      .scaleSequential()
      .domain([0, maxPopularity])
      .interpolator(d3.interpolateBlues);

    const bubbleGroup = g.append("g");

    const updateBubbles = () => {
      const bubbles = bubbleGroup
        .selectAll("circle")
        .data(songDataByCountry, (d) => d.country); // Use country as key for better data binding

      // Enter + Update
      bubbles
        .join("circle")
        .attr("cx", (d) => {
          const countryFeature = countries.features.find(
            (f) => f.properties.name === d.country
          );
          if (!countryFeature) return null;
          const coords = projection(d3.geoCentroid(countryFeature));
          return coords ? coords[0] : null;
        })
        .attr("cy", (d) => {
          const countryFeature = countries.features.find(
            (f) => f.properties.name === d.country
          );
          if (!countryFeature) return null;
          const coords = projection(d3.geoCentroid(countryFeature));
          return coords ? coords[1] : null;
        })
        .attr("r", (d) => bubbleScale(d.popularity))
        .attr("fill", (d) => colorScale(d.popularity))
        .attr("opacity", 0.7)
        .on("click", (event, d) => {
          setCountry(d.country);
        })
        .on("mouseover", (event, d) => {
          tooltip
            .style("visibility", "visible")
            .html(`<b>${d.country}</b><br />Ranking: ${d.daily_rank}`);
        })
        .on("mousemove", (event) => {
          tooltip
            .style("top", `${event.pageY - 10}px`)
            .style("left", `${event.pageX + 10}px`);
        })
        .on("mouseout", () => {
          tooltip.style("visibility", "hidden");
        });
    };

    updateBubbles();

    const zoom = d3
      .zoom()
      .scaleExtent([1, 8])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
        updateBubbles(); 
      });

    svg.call(zoom);

    return () => {
      tooltip.remove();
      svg.on(".zoom", null);
    };
  }, [data, song, setCountry]);

  const information = {
    "About this Visualization" : "This bubble map displays the ranking of a previously selected song across the entire world",
    "Key Features": [
      "The countries that have the selected song in the top 10 list will have a blue bubble indicating the ranking in that specific country",
      "If the country doesn't have it then, no blue bubble will be shown",
      "In this chart its not possible to select a country, only to visualize the ranking of a selected song in different countries",
      "Zoom in and zoom out in the map"
    ],
    "How to use": "Select a song from the top 10 list of the world or a specific country and bubbles will be displayed in the map. If you hover through each bubble the name of the country and the ranking will appear. To remove this visualization simply deselect the song in the top 10 list."
  };

  return (
    <div className="flex flex-col items-center">
      <span className="flex flex-row justify-between items-center w-full">
        <h1 className="font-semibold">
          Ranking of the song{" "}
          <span className="underline italic text-green-500">{song.name}</span> by{" "}
          <span className="underline italic text-green-500">{song.artists}</span>{" "}
          across the world
        </h1>
        <HelpPopHover information={information} placement="bottom" />
      </span>
      <svg id="bubble-map"></svg>
    </div>
  );
};

export default BubbleMap;
