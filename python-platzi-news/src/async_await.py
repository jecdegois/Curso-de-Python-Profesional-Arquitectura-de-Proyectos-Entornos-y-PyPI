import asyncio
import logging
import time

logging.basicConfig(level=logging.DEBUG)


async def tarea(nombre: str, segundos: int) -> str:
    inicio = time.perf_counter()
    logging.info(f"Inicio {nombre} ({segundos}s)")
    await asyncio.sleep(segundos)
    fin = time.perf_counter()
    logging.info(f"Fin {nombre} - tomó {fin - inicio:.2f} seg")
    return f"{nombre}: completada"


async def main() -> None:
    inicio_total = time.perf_counter()
    logging.info("=== Inicio programa ASYNC ===")
    resultados = await asyncio.gather(
        tarea("A", 3),
        tarea("B", 2),
        tarea("C", 1),
        tarea("D", 3),
    )

    fin_total = time.perf_counter()
    logging.info(
        f"=== Fin programa ASYNC - total {fin_total - inicio_total:.2f} seg ==="
    )
    print("Resultados:", resultados)


# asyncio.run(main())

my_loop = asyncio.new_event_loop()
my_loop.set_debug(True)
asyncio.set_event_loop(loop=my_loop)


try:
    my_loop.run_until_complete(main())
finally:
    my_loop.close()
