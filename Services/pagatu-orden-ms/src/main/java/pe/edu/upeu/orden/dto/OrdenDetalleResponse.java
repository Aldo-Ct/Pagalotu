package pe.edu.upeu.orden.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class OrdenDetalleResponse {
    private Long id;
    private Long productoId;
    private Integer cantidad;
    private BigDecimal precioUnitario;
}
