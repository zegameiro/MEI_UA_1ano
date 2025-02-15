import { useEffect, useRef } from "react";
import * as d3 from "d3";

import HelpPopHover from "./HelpPopOver";

const LineChart = ({ data, country }) => {
  const svgRef = useRef();

  const interpolatePositions = (start, end) => {
    const step = (end - start) / 6;
    return Array.from({ length: 7 }, (_, i) => start + i * step);
  };

  const prepareChartData = (data) => {
    return data.map((item) => {
      const currentPos = parseInt(item.daily_rank);
      const weekly_movement = parseInt(item.weekly_movement);
      const lastWeekPos =
        weekly_movement == 0 ? currentPos : currentPos + weekly_movement;

      const positions = interpolatePositions(lastWeekPos, currentPos).map(
        (position, i) => ({
          date: d3.timeFormat("%Y-%m-%d")(
            d3.timeDay.offset(new Date(item.snapshot_date), -6 + i)
          ),
          position,
        })
      );

      return {
        name: item.name,
        positions,
      };
    });
  };

  useEffect(() => {
    const dataCountry = data.filter((d) =>
      country ? d.country === country : d.country === ""
    );

    const chartData = prepareChartData(dataCountry);

    const margin = { top: 20, right: 30, bottom: 50, left: 50 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3
      .select(svgRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const allDates = Array.from(
      new Set(chartData.flatMap((song) => song.positions.map((p) => p.date)))
    );

    const xScale = d3.scalePoint().domain(allDates).range([0, width]);

    console.log(chartData)

    const yScale = d3
      .scaleLinear()
      .domain([
        d3.max(chartData, (d) => d3.max(d.positions, (p) => p.position)) + 1,
        d3.min(chartData, (d) => d3.min(d.positions, (p) => p.position)) - 1,
      ])
      .range([height, 0]);

    const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale);

    svg.append("g").attr("transform", `translate(0, ${height})`).call(xAxis);

    svg
      .append("text")
      .attr("x", width / 2) // Center horizontally
      .attr("y", height + margin.bottom - 10) // Position below the x-axis
      .attr("text-anchor", "middle") // Align center
      .attr("font-size", "14px")
      .attr("fill", "white")
      .text("Day of the week");

    svg.append("g").call(yAxis);

    svg
      .append("text")
      .attr("x", -height / 2)
      .attr("y", -margin.left + 15)
      .attr("text-anchor", "middle")
      .attr("font-size", "14px")
      .attr("fill", "white")
      .attr("transform", "rotate(-90)")
      .text("Ranking");

    const points = [];
    const path = svg
      .append("g")
      .selectAll(".line")
      .data(chartData)
      .join("path")
      .attr("class", "line")
      .attr("fill", "steelblue")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 2)
      .attr("d", (d) =>
        d3
          .line()
          .x((p) => xScale(p.date))
          .y((p) => yScale(p.position))(d.positions)
      )
      .each((d) => {
        d.positions.forEach((p) => {
          points.push([
            xScale(p.date),
            yScale(p.position),
            d.name,
            d3.format(".0f")(p.position),
          ]);
        });
      });

    // Add points
    svg
      .append("g")
      .selectAll(".point")
      .data(
        chartData.flatMap((song) =>
          song.positions.map((p) => ({
            date: p.date,
            position: p.position,
            name: song.name,
          }))
        )
      )
      .join("circle")
      .attr("class", "point")
      .attr("cx", (d) => xScale(d.date))
      .attr("cy", (d) => yScale(d.position))
      .attr("r", 4)
      .attr("fill", "red")
      .attr("stroke", "white")
      .attr("stroke-width", 1);

    const dot = svg.append("g").attr("display", "none");

    dot.append("circle").attr("r", 4.5).attr("fill", "red");

    dot.append("text").attr("font-size", "12px").attr("dy", "-0.7em");

    function pointermoved(event) {
      const [xm, ym] = d3.pointer(event);
      const i = d3.leastIndex(points, ([x, y]) => Math.hypot(x - xm, y - ym));
      const [x, y, name, position] = points[i];
      path
        .style("stroke", ({ name: z }) => (z === name ? "steelblue" : "gray"))
        .filter(({ name: z }) => z === name)
        .raise();
      dot.attr("transform", `translate(${x},${y})`);
      dot
        .select("text")
        .attr("x", -10)
        .attr("y", 0)
        .attr("text-anchor", "end")
        .text(`${name}: Position ${position}`)
        .attr("fill", "white");
    }

    function pointerentered() {
      dot.attr("display", null);
    }

    function pointerleft() {
      path.style("stroke", "steelblue");
      dot.attr("display", "none");
    }

    svg
      .on("pointermove", pointermoved)
      .on("pointerenter", pointerentered)
      .on("pointerleave", pointerleft);
  }, [data, country]);

  const information = {
    "About this Visualization" : "Line Chart that displays the changes that occured in the rankings of the top 10 songs in a given country or the entire world, in a full week",
    "Key Features": [
      "Each line represents a song from the top 10 list of a country or the entire world",
      "If the line is growing than it means that song rose up in the top 10 list ranking",
      "If the line is decreasing than the song came down in the ranking",
      "If the line is constant (has always the same values) it means that the song maintained the same ranking during the entire week"
    ],
    "How to use": "To learn which line belongs to which song, simply hover over the red dots on each line and you'll learn the song thats being represented. It will also present the ranking value at a given date"
  }

  return (
    <div className="flex flex-col items-center ">
      <span className="flex flex-row justify-between items-center">
        <h1 className="font-semibold w-3/4 text-lg">
          Change in rankings of the 10 top songs in{" "}
          {country != "" ? country : "the World"} compared to the previous week
        </h1>
        <HelpPopHover information={information} placement="left" />
      </span>
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default LineChart;
