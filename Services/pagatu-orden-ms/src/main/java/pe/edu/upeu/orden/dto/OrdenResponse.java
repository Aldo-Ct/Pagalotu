package pe.edu.upeu.orden.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import pe.edu.upeu.orden.entity.MetodoPago;
import pe.edu.upeu.orden.entity.MomentoPago;
import pe.edu.upeu.orden.entity.TipoComprobante;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class OrdenResponse {
    private Long id;
    private Long clienteId;
    private LocalDateTime fechaCreacion;
    private String estado;
    private TipoComprobante tipoComprobante;
    private MetodoPago metodoPago;
    private MomentoPago momentoPago;
    private BigDecimal total;
    private List<OrdenDetalleResponse> detalles;
}
