import { useEffect, useRef } from "react";
import * as d3 from "d3";

import HelpPopHover from "./HelpPopOver";

const BarChart = ({ data, country }) => {
  const svgRef = useRef();

  useEffect(() => {
    const chartData = data.filter((d) => (country ? d.country === country : d.country === ""));

    const width = 928;
    const height = 500;
    const margin = { top: 30, right: 0, bottom: 30, left: 40 };

    d3.select(svgRef.current).selectAll("*").remove();

    const x = d3.scaleBand()
      .domain(chartData.map(d => d.daily_rank))
      .range([margin.left, width - margin.right])
      .padding(0.1);

    const y = d3.scaleLinear()
      .domain([0, d3.max(chartData, (d) => parseInt(d.popularity))])
      .range([height - margin.bottom, margin.top]);

    const svg = d3.select(svgRef.current)
     .attr("width", width)
     .attr("height", height)
     .attr("viewBox", [0, 0, width, height])
     .attr("style", "max-width: 100%; height: auto");

    const tooltip = d3.select("body")
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

    svg
      .append("text")
      .attr("x", width / 2) // Center horizontally
      .attr("y", height + margin.bottom - 10) // Position below the x-axis
      .attr("text-anchor", "middle") // Align center
      .attr("font-size", "14px")
      .attr("fill", "white")
      .text("Day of the week");

    svg.append("g")
        .attr("fill", "steelblue")
      .selectAll()
      .data(chartData)
      .join("rect")
        .attr("x", (d) => x(d.daily_rank))
        .attr("y", (d) => y(parseInt(d.popularity)))
        .attr("height", (d) => y(0) - y(parseInt(d.popularity)))
        .attr("width", x.bandwidth())
        .on("mouseover", (event, d) => {
          tooltip.style("visibility", "visible")
            .html(`${d.name}<br>Popularity: ${d.popularity}`);
        })
        .on("mousemove", event => {
          tooltip.style("top", `${event.pageY - 10}px`)
            .style("left", `${event.pageX + 10}px`);
        })
        .on("mouseout", () => {
          tooltip.style("visibility", "hidden");
        });

    svg.append("g")
      .attr("transform", `translate(0, ${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickSizeOuter(0));

    svg.append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .call(g => g.select(".domain").remove())
      .call(g => g.append("text")
          .attr("x", -margin.left)
          .attr("y", 10)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text("Popularity"));

  }, [data, country]);

  const information = {
    "About this Visualization" : "Bar chart that presents the popularity values of each song from the top 10 list of a given country or the entire world.",
    "Key Features": [
      "The x axis presents the ranking of each song with ascending order",
      "The y axis presents the possible popularity values for the songs",
      "Each bar represents a song in the list",
    ],
    "How to use": "To identify each song you can hover over each bar and learn which song is being represented, the popularity value is also presented."
  }

  return (
    <div className="flex flex-col space-y-10 text-center">
      <span className="flex flex-row items-center justify-between">
        <h1 className="font-semibold">Popularity of the top 10 Songs in {country != "" ? country : "the World"} </h1>
        <HelpPopHover information={information} placement="left" />
      </span>
      <svg ref={svgRef}></svg>
    </div>
  )

};

export default BarChart;
