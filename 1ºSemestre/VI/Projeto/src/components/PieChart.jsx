import { useEffect, useRef } from "react";
import * as d3 from "d3";

import HelpPopHover from "./HelpPopOver";

const PieChart = ({ data, country }) => {
  const ref = useRef();

  useEffect(() => {
    const d = data.filter((d) => (country ? d.country === country : d.country === ""));
    console.log(d)
    const da = d3.group(d, (song) => song.is_explicit);

    const chart_data = [
      {
        name: "Non Explicit",
        value: da?.get("False")?.length,
      },
      {
        name: "Explicit",
        value: da?.get("True")?.length,
      },
    ];

    d3.select(ref.current).selectAll("*").remove();

    const width = 200;
    const height = 200;
    const radius = Math.min(width, height) / 2;

    const arc = d3.arc()
      .innerRadius(radius * 0.67)
      .outerRadius(radius - 1)

    const color = d3.scaleOrdinal()
      .domain(chart_data.map(d => d.name))
      .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), chart_data.length).reverse())

    const pie = d3.pie()
      .padAngle(1 / radius)
      .sort(null)
      .value(d => d.value);

    const svg = d3.select(ref.current)
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("style", "max-width: 100%; height: auto");

    svg.append("g")
      .selectAll()
      .data(pie(chart_data))
      .join("path")
      .attr("fill", (d) => color(d.data.name))
      .attr("d", arc);

    svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 12)
        .attr("text-anchor", "middle")
      .selectAll()
      .data(pie(chart_data))
      .join("text")
        .attr("transform", (d) => `translate(${arc.centroid(d)})`)
        .call((text) => text.append("tspan")
            .attr("y", "-0.4em")
            .attr("font-weight", "bold")
            .attr("fill", "white")
            .text((d) => d.data.name)
        )
        .call((text) => text.filter((d) => d.endAngle - d.startAngle > 0.25).append("tspan")
            .attr("x", 0)
            .attr("y", "0.7em")
            .attr("fill", "white")
            .attr("fill-opacity", 0.7)
            .text((d) => d.data.value.toLocaleString("en-US"))
        );
  }, [data, country]);

  const information = {
    "About this Visualization" : "A Pie Chart that shows the total number of songs that are considered Explicit and Non Explicit for a given country or the entire world.",
    "Key Features": [
      "The number of explicit songs is represented with the color red where the number is also displayed",
      "The number of non explicit songs is presented with the blue color, and the number is also displayed",
    ],
  }

  return (
    <div className="flex flex-col items-center space-y-10 w-full">
      <span className="flex flex-row items-center justify-between w-full">
        <h1 className="font-semibold">Number of Explicit and Non Explicit songs</h1>
        <HelpPopHover information={information} placement="left" />
      </span>
      <svg ref={ref}></svg>
    </div>
  );
};

export default PieChart;
